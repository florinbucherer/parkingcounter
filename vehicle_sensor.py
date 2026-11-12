import sys
import threading
import time
from collections import deque
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from sensor_interface import Direction, ISensor


TRACKING_DIR = (
    Path(__file__).resolve().parent
    / "CarDetector&Counter_Branch"
    / "Real-Time-Vehicle-Detection-Tracking-and-Counting-in-Python"
)
DEFAULT_VIDEO_PATH = TRACKING_DIR / "cars2.mp4"
DEFAULT_OUTPUT_PATH = TRACKING_DIR / "vehicle_sensor_output.mp4"

Point = Tuple[int, int]


class VehicleSensor(ISensor):
    """Detects and tracks vehicles, adding one event per line crossing."""

    def __init__(
        self,
        events: list,
        video_path: Union[str, Path, int] = DEFAULT_VIDEO_PATH,
        output_path: Union[str, Path] = DEFAULT_OUTPUT_PATH,
        display: bool = True,
    ):
        super().__init__(events)
        self.video_path = video_path
        self.output_path = Path(output_path)
        self.display = display
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            raise RuntimeError("Vehicle sensor is already running")
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    @staticmethod
    def _crossing_direction(
        previous: Point,
        current: Point,
        line_x: int = 750,
        line_top: int = 200,
        line_bottom: int = 700,
    ) -> Optional[Direction]:
        if current[0] == previous[0]:
            return None
        if previous[0] < line_x <= current[0]:
            direction = Direction.OUT
        elif previous[0] > line_x >= current[0]:
            direction = Direction.IN
        else:
            return None

        crossing_y = previous[1] + (
            (current[1] - previous[1]) * (line_x - previous[0])
            / (current[0] - previous[0])
        )
        return direction if line_top <= crossing_y <= line_bottom else None

    def _run(self):
        import cv2
        import numpy as np
        from ultralytics import YOLO

        if str(TRACKING_DIR) not in sys.path:
            sys.path.insert(0, str(TRACKING_DIR))

        from deep_sort.deep_sort.tracker import Tracker
        from deep_sort.deep_sort import nn_matching
        from deep_sort.deep_sort.detection import Detection
        from deep_sort.tools import generate_detections as gdet

        video_cap = None
        writer = None
        try:
            video_cap = cv2.VideoCapture(self.video_path)
            if not video_cap.isOpened():
                raise RuntimeError("Could not open video source: {}".format(self.video_path))

            fps = video_cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0:
                fps = 30
            width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            writer = cv2.VideoWriter(
                str(self.output_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (width, height),
            )
            if not writer.isOpened():
                raise RuntimeError(
                    "Could not open output video for writing: {}".format(self.output_path)
                )

            model = YOLO(str(TRACKING_DIR / "yolov8s.pt"))
            encoder = gdet.create_box_encoder(
                str(TRACKING_DIR / "config" / "mars-small128.pb"),
                batch_size=1,
            )
            metric = nn_matching.NearestNeighborDistanceMetric(
                "cosine", 0.4, None
            )
            tracker = Tracker(metric)

            with open(TRACKING_DIR / "config" / "coco.names", encoding="utf-8") as file:
                class_names = file.read().splitlines()

            np.random.seed(42)
            colors = np.random.randint(0, 255, size=(len(class_names), 3))
            points: Dict[int, deque] = {}
            crossing_total = 0
            line_x = 750
            line_top, line_bottom = 200, 700
            vehicle_classes = {"car", "motorcycle", "bus", "truck"}

            while not self._stop_event.is_set():
                frame_start = time.perf_counter()
                ret, frame = video_cap.read()
                if not ret:
                    break

                cv2.line(frame, (line_x, line_bottom), (line_x, line_top), (0, 0, 255), 12)
                results = model(frame, verbose=False)
                bboxes = []
                confidences = []
                class_ids = []

                for result in results:
                    if result.boxes is None:
                        continue
                    for data in result.boxes.data.tolist():
                        x1, y1, x2, y2, confidence, class_id = data
                        class_id = int(class_id)
                        if (
                            confidence > 0.3
                            and 0 <= class_id < len(class_names)
                            and class_names[class_id] in vehicle_classes
                        ):
                            bboxes.append(
                                [int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1)]
                            )
                            confidences.append(confidence)
                            class_ids.append(class_id)

                names = [class_names[class_id] for class_id in class_ids]
                features = encoder(frame, bboxes)
                detections = [
                    Detection(bbox, confidence, class_name, feature)
                    for bbox, confidence, class_name, feature in zip(
                        bboxes, confidences, names, features
                    )
                ]
                tracker.predict()
                tracker.update(detections)

                for track in tracker.tracks:
                    if not track.is_confirmed() or track.time_since_update > 1:
                        continue

                    x1, y1, x2, y2 = (int(value) for value in track.to_tlbr())
                    class_name = track.get_class()
                    color = colors[class_names.index(class_name)]
                    color_bgr = tuple(int(channel) for channel in color)
                    text = "{} - {}".format(track.track_id, class_name)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, 3)
                    cv2.putText(
                        frame,
                        text,
                        (x1 + 5, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (255, 255, 255),
                        2,
                    )

                    center = ((x1 + x2) // 2, (y1 + y2) // 2)
                    history = points.setdefault(track.track_id, deque(maxlen=32))
                    if history:
                        direction = self._crossing_direction(
                            history[-1], center, line_x, line_top, line_bottom
                        )
                        if direction is not None:
                            self.events.append(direction)
                            crossing_total += direction.value

                    history.append(center)
                    cv2.circle(frame, center, 4, (0, 255, 0), -1)
                    for index in range(1, len(history)):
                        cv2.line(frame, history[index - 1], history[index], (0, 255, 0), 2)

                elapsed = time.perf_counter() - frame_start
                fps = 1 / elapsed if elapsed > 0 else 0
                cv2.putText(
                    frame,
                    "FPS: {:.2f}".format(fps),
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    "Crossings: {}".format(crossing_total),
                    (50, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                )

                writer.write(frame)
                if self.display:
                    cv2.imshow("Vehicle Detection", frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key in (ord("q"), ord("Q")):
                        self._stop_event.set()
                    elif key in (ord("p"), ord("P")):
                        while not self._stop_event.is_set():
                            key = cv2.waitKey(50) & 0xFF
                            if key in (ord("p"), ord("P"), ord("q"), ord("Q")):
                                if key in (ord("q"), ord("Q")):
                                    self._stop_event.set()
                                break
        finally:
            if video_cap is not None:
                video_cap.release()
            if writer is not None:
                writer.release()
            if self.display:
                cv2.destroyAllWindows()
