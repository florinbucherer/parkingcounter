import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import vehicle_sensor
from sensor_interface import Direction
from vehicle_sensor import VehicleSensor

IN = Direction.IN    # car comes in
OUT = Direction.OUT  # car goes out

# A small fake detector. It replaces the real camera code (YOLO, DeepSORT).
FAKE_DETECTOR = """
from sensor_interface import Direction


def detect_crossings(crossing_function, video_path, output_path=None, stop_event=None, display=True):
    # only send IN if the arguments are the expected ones
    if video_path == "test.mp4" and display is False and stop_event is not None:
        yield Direction.IN
    yield Direction.OUT
"""


class TestCrossingDirection(unittest.TestCase):
    # the default line is at x = 750, from y = 200 to y = 700

    def test_same_x_is_ignored(self):
        self.assertIsNone(VehicleSensor._crossing_direction((750, 300), (750, 400)))

    def test_touching_the_line_from_left_is_exit(self):
        self.assertEqual(VehicleSensor._crossing_direction((749, 400), (750, 400)), OUT)

    def test_leaving_the_line_to_the_right_is_ignored(self):
        # the car already was on the line, so it crossed before
        self.assertIsNone(VehicleSensor._crossing_direction((750, 400), (751, 400)))

    def test_touching_the_line_from_right_is_entry(self):
        self.assertEqual(VehicleSensor._crossing_direction((751, 400), (750, 400)), IN)

    def test_crossing_at_top_end_counts(self):
        self.assertEqual(VehicleSensor._crossing_direction((740, 200), (760, 200)), OUT)

    def test_crossing_at_bottom_end_counts(self):
        self.assertEqual(VehicleSensor._crossing_direction((760, 700), (740, 700)), IN)

    def test_crossing_below_the_line_is_ignored(self):
        self.assertIsNone(VehicleSensor._crossing_direction((740, 701), (760, 701)))

    def test_diagonal_crossing_uses_crossing_point(self):
        # starts above the line but crosses at y = 150 + 0.5 * 500 = 400 -> inside
        self.assertEqual(VehicleSensor._crossing_direction((700, 150), (800, 650)), OUT)

    def test_diagonal_crossing_outside_is_ignored(self):
        # crosses at y = 0 + 0.5 * 100 = 50 -> outside the line
        self.assertIsNone(VehicleSensor._crossing_direction((700, 0), (800, 100)))

    def test_own_line_values(self):
        self.assertEqual(
            VehicleSensor._crossing_direction((90, 5), (110, 5), line_x=100, line_top=0, line_bottom=10),
            OUT,
        )


class TestVehicleSensorInit(unittest.TestCase):

    def test_default_values(self):
        events = []
        s = VehicleSensor(events)
        self.assertIs(s.events, events)
        self.assertEqual(s.video_path, vehicle_sensor.DEFAULT_VIDEO_PATH)
        self.assertEqual(s.output_path, vehicle_sensor.DEFAULT_OUTPUT_PATH)
        self.assertTrue(s.display)

    def test_own_values(self):
        s = VehicleSensor([], video_path=0, output_path="out.mp4", display=False)
        self.assertEqual(s.video_path, 0)       # 0 = webcam
        self.assertEqual(s.output_path, Path("out.mp4"))   # text becomes a Path
        self.assertFalse(s.display)


class TestVehicleSensorStartStop(unittest.TestCase):

    def make_sensor(self):
        s = VehicleSensor([])
        # fake _run: only waits until stop() is called
        s._run = lambda: s._stop_event.wait()
        return s

    def test_start_runs_a_thread(self):
        s = self.make_sensor()
        s.start()
        self.assertTrue(s._thread.is_alive())
        s.stop()

    def test_stop_ends_the_thread(self):
        s = self.make_sensor()
        s.start()
        s.stop()
        self.assertIsNone(s._thread)
        self.assertTrue(s._stop_event.is_set())

    def test_second_start_raises_error(self):
        s = self.make_sensor()
        s.start()
        with self.assertRaises(RuntimeError):
            s.start()
        s.stop()

    def test_stop_without_start(self):
        s = VehicleSensor([])
        s.stop()   # must not crash
        self.assertTrue(s._stop_event.is_set())

    def test_start_again_after_stop(self):
        s = self.make_sensor()
        s.start()
        s.stop()
        s.start()
        self.assertTrue(s._thread.is_alive())
        self.assertFalse(s._stop_event.is_set())
        s.stop()


class TestVehicleSensorRun(unittest.TestCase):

    def setUp(self):
        # temp folder with the fake detector instead of the real one
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        (Path(self.folder.name) / "object_detection_tracking.py").write_text(FAKE_DETECTOR)
        patcher = patch("vehicle_sensor.TRACKING_DIR", Path(self.folder.name))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.remove_from_path)

    def remove_from_path(self):
        while self.folder.name in sys.path:
            sys.path.remove(self.folder.name)

    def test_events_are_queued(self):
        events = []
        s = VehicleSensor(events, video_path="test.mp4", display=False)
        s._run()
        self.assertEqual(events, [IN, OUT])

    def test_wrong_arguments_give_other_events(self):
        events = []
        s = VehicleSensor(events, video_path="other.mp4", display=False)
        s._run()
        self.assertEqual(events, [OUT])

    def test_folder_is_added_to_path_only_once(self):
        s = VehicleSensor([], video_path="test.mp4", display=False)
        s._run()
        s._run()
        self.assertEqual(sys.path.count(self.folder.name), 1)

    def test_missing_module_spec_raises_error(self):
        s = VehicleSensor([])
        with patch("vehicle_sensor.importlib.util.spec_from_file_location", return_value=None):
            with self.assertRaises(ImportError):
                s._run()

    def test_works_inside_the_thread(self):
        events = []
        s = VehicleSensor(events, video_path="test.mp4", display=False)
        s.start()
        s.stop()   # waits until the thread is done
        self.assertEqual(events, [IN, OUT])
