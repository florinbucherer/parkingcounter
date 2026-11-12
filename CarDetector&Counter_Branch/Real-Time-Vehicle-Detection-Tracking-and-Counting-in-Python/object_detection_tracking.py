import sys
import threading
from collections import deque
from pathlib import Path
from typing import Callable, Dict, Iterator, Optional, Tuple, TypeVar, Union


BASE_DIR = Path(__file__).resolve().parent
Point = Tuple[int, int]
Event = TypeVar("Event")
CrossingDirection = Callable[
    [Point, Point, int, int, int], Optional[Event]
]


def detect_crossings(
    crossing_direction: CrossingDirection,
    video_path: Union[str, Path, int] = BASE_DIR / "cars2.mp4",
    output_path: Optional[Union[str, Path]] = BASE_DIR / "output.mp4",
    stop_event: Optional[threading.Event] = None,
    display: bool = True,
) -> Iterator[Event]:
    """Track vehicles and yield the direction returned for each line crossing."""
    import cv2
    import numpy as np
    from ultralytics import YOLO

    from deep_sort.deep_sort.tracker import Tracker
    from deep_sort.deep_sort import nn_matching
    from deep_sort.deep_sort.detection import Detection
    from deep_sort.tools import generate_detections as gdet

    if stop_event is None:
        stop_event = threading.Event()

    video_cap = None
    writer = None
    try:
        video_cap = cv2.VideoCapture(video_path)
        if not video_cap.isOpened():
            raise RuntimeError("Could not open video source: {}".format(video_path))

        fps = video_cap.get(cv2.CAP_PROP_FPS)
        if fps <= 0:
            fps = 30
        width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            writer = cv2.VideoWriter(
                str(output_path),
                cv2.VideoWriter_fourcc(*"mp4v"),
                fps,
                (width, height),
            )
            if not writer.isOpened():
                raise RuntimeError(
                    "Could not open output video for writing: {}".format(output_path)
                )

        model = YOLO(str(BASE_DIR / "yolov8s.pt"))
        encoder = gdet.create_box_encoder(
            str(BASE_DIR / "config" / "mars-small128.pb"),
            batch_size=1,
        )
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", 0.4, None)
        tracker = Tracker(metric)

        with open(BASE_DIR / "config" / "coco.names", encoding="utf-8") as file:
            class_names = file.read().splitlines()

        np.random.seed(42)
        colors = np.random.randint(0, 255, size=(len(class_names), 3))
        points: Dict[int, deque] = {}
        line_x = int(width * 750 / 1280)
        line_top = int(height * 200 / 720)
        line_bottom = int(height * 700 / 720)
        vehicle_classes = {"car", "motorcycle", "bus", "truck"}

        while not stop_event.is_set():
            ret, frame = video_cap.read()
            if not ret:
                break

            cv2.line(
                frame,
                (line_x, line_bottom),
                (line_x, line_top),
                (0, 0, 255),
                12,
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
                direction = None
                if history:
                    direction = crossing_direction(
                        history[-1], center, line_x, line_top, line_bottom
                    )

                history.append(center)
                cv2.circle(frame, center, 4, (0, 255, 0), -1)
                for index in range(1, len(history)):
                    cv2.line(frame, history[index - 1], history[index], (0, 255, 0), 2)

                if direction is not None:
                    history.clear()
                    history.append(center)
                    yield direction

            if writer is not None:
                writer.write(frame)

            if display:
                cv2.imshow("Vehicle Detection", frame)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), ord("Q")):
                    stop_event.set()
                elif key in (ord("p"), ord("P")):
                    while not stop_event.is_set():
                        key = cv2.waitKey(50) & 0xFF
                        if key in (ord("p"), ord("P"), ord("q"), ord("Q")):
                            if key in (ord("q"), ord("Q")):
                                stop_event.set()
                            break
    finally:
        if video_cap is not None:
            video_cap.release()
        if writer is not None:
            writer.release()
        if display:
            cv2.destroyAllWindows()


def main():
    sys.path.insert(0, str(BASE_DIR.parent.parent))
    from vehicle_sensor import VehicleSensor

    for direction in detect_crossings(VehicleSensor._crossing_direction):
        print(direction.name)


if __name__ == "__main__":
    main()
