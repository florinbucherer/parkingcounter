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
WEBCAM_INDEX = 0   # 0 = first webcam of the computer, 1 = second one, ...

# The counting line is a vertical line in the middle of the image, from 10 % to 90 %
# of the height. So it fits every camera and resolution without any setting.
# A car driving from right to left counts as IN, from left to right as OUT.
LINE_TOP_RATIO = 0.1
LINE_BOTTOM_RATIO = 0.9

Point = Tuple[int, int]


class VehicleSensor(ISensor):
    """Detects and tracks vehicles, adding one event per line crossing.

    By default it uses the first webcam and does not record anything.
    To test with a video file instead: VehicleSensor(events, video_path=DEFAULT_VIDEO_PATH)

    video_path: an int is a webcam index (0 = first webcam),
                a str / Path is a video file.
    output_path: where to record the annotated video, None = do not record
                 (a live webcam would make the file grow forever).
    """

    def __init__(
        self,
        events: list,
        video_path: Union[str, Path, int] = WEBCAM_INDEX,
        output_path: Optional[Union[str, Path]] = None,
        display: bool = True,
    ):
        super().__init__(events)
        self.video_path = video_path
        self.output_path = Path(output_path) if output_path is not None else None
        self.display = display
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._cap = None

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            raise RuntimeError("Vehicle sensor is already running")
        self._stop_event.clear()
        # Open the camera here (not in the thread), so a missing or busy webcam
        # stops the program with a clear message instead of failing silently.
        self._cap = self._open_capture()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
            self._thread = None
        self._cap = None

    @staticmethod
    def _capture_source(video_path: Union[str, Path, int]) -> Union[str, int]:
        """cv2.VideoCapture wants an int (webcam) or a str (file), not a Path."""
        return video_path if isinstance(video_path, int) else str(video_path)

    def _open_capture(self):
        import cv2

        source = self._capture_source(self.video_path)
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            cap.release()
            if isinstance(source, int):
                raise RuntimeError(
                    "Could not open webcam {}. Is it plugged in, not used by another "
                    "program, and is the camera permission granted? "
                    "(try another index, e.g. --camera 1)".format(source)
                )
            raise RuntimeError("Could not open video file: {}".format(source))
        return cap

    @staticmethod
    def _counting_line(width: int, height: int) -> Tuple[int, int, int]:
        """Pixel position (line_x, line_top, line_bottom) of the line for this frame size."""
        return (
            width // 2,
            int(round(height * LINE_TOP_RATIO)),
            int(round(height * LINE_BOTTOM_RATIO)),
        )

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
        import cv2   # already imported successfully by start(), needed in finally below

        video_cap = self._cap   # opened in start()
        writer = None
        try:
            import numpy as np
            from ultralytics import YOLO

            if str(TRACKING_DIR) not in sys.path:
                sys.path.insert(0, str(TRACKING_DIR))

            from deep_sort.deep_sort.tracker import Tracker
            from deep_sort.deep_sort import nn_matching
            from deep_sort.deep_sort.detection import Detection
            from deep_sort.tools import generate_detections as gdet

            if self.output_path is not None:
                fps = video_cap.get(cv2.CAP_PROP_FPS)
                if fps <= 0:
                    fps = 30   # many webcams do not report their fps
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
            vehicle_classes = {"car", "motorcycle", "bus", "truck"}

            while not self._stop_event.is_set():
                frame_start = time.perf_counter()
                ret, frame = video_cap.read()
                if not ret:
                    print("Vehicle sensor: no more frames from {}".format(self.video_path))
                    break

                # the line is always in the middle of the image, whatever the camera size
                line_x, line_top, line_bottom = self._counting_line(
                    frame.shape[1], frame.shape[0]
                )
                cv2.line(
                    frame,
                    (line_x, line_bottom),
                    (line_x, line_top),
                    (0, 0, 255),
                    max(2, frame.shape[0] // 90),   # 12 px on 1080p, thinner on small frames
                )
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
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color_bgr, 3)

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

                if writer is not None:
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