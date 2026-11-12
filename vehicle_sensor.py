import importlib.util
import sys
import threading
from pathlib import Path
from typing import Optional, Tuple, Union

from sensor_interface import Direction, ISensor


TRACKING_DIR = (
    Path(__file__).resolve().parent
    / "CarDetector&Counter_Branch"
    / "Real-Time-Vehicle-Detection-Tracking-and-Counting-in-Python"
)
DEFAULT_VIDEO_PATH = 0      # 0 = Standard-Webcam (bei mehreren Kameras 1, 2, ...)
DEFAULT_OUTPUT_PATH = None  # keine Aufnahme mitschreiben
Point = Tuple[int, int]


class VehicleSensor(ISensor):
    """Runs vehicle detection and queues each detected crossing direction."""

    def __init__(
        self,
        events: list,
        video_path: Union[str, Path, int] = DEFAULT_VIDEO_PATH,
        output_path: Optional[Union[str, Path]] = DEFAULT_OUTPUT_PATH,
        display: bool = True,
    ):
        super().__init__(events)
        self.video_path = video_path
        self.output_path = Path(output_path) if output_path is not None else None
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
        if str(TRACKING_DIR) not in sys.path:
            sys.path.insert(0, str(TRACKING_DIR))

        module_path = TRACKING_DIR / "object_detection_tracking.py"
        spec = importlib.util.spec_from_file_location(
            "parkingcounter_object_detection_tracking", module_path
        )
        if spec is None or spec.loader is None:
            raise ImportError("Could not load detector module from {}".format(module_path))
        detector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(detector)

        for direction in detector.detect_crossings(
            self._crossing_direction,
            self.video_path,
            output_path=self.output_path,
            stop_event=self._stop_event,
            display=self.display,
        ):
            self.events.append(direction)