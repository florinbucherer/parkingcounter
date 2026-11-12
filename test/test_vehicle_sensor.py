import importlib.util
import unittest
from pathlib import Path

from sensor_interface import Direction
from vehicle_sensor import VehicleSensor


class TestVehicleSensorCrossings(unittest.TestCase):
    def test_left_to_right_is_exit(self):
        self.assertEqual(
            VehicleSensor._crossing_direction((740, 400), (760, 400)),
            Direction.OUT,
        )

    def test_right_to_left_is_entry(self):
        self.assertEqual(
            VehicleSensor._crossing_direction((760, 400), (740, 400)),
            Direction.IN,
        )

    def test_does_not_count_motion_that_does_not_cross(self):
        self.assertIsNone(
            VehicleSensor._crossing_direction((720, 400), (740, 400))
        )

    def test_does_not_count_crossing_outside_line_segment(self):
        self.assertIsNone(
            VehicleSensor._crossing_direction((740, 100), (760, 100))
        )


class TestVehicleSensorWebcam(unittest.TestCase):
    def test_line_is_in_the_middle_of_a_webcam_image(self):
        self.assertEqual(VehicleSensor._counting_line(640, 480), (320, 48, 432))

    def test_line_is_in_the_middle_of_a_full_hd_image(self):
        self.assertEqual(VehicleSensor._counting_line(1920, 1080), (960, 108, 972))

    def test_default_source_is_the_first_webcam_without_recording(self):
        sensor = VehicleSensor([])
        self.assertEqual(sensor.video_path, 0)
        self.assertIsNone(sensor.output_path)

    def test_webcam_index_is_passed_on_as_int(self):
        self.assertEqual(VehicleSensor._capture_source(0), 0)

    def test_video_path_is_passed_on_as_str(self):
        source = VehicleSensor._capture_source(Path("some") / "video.mp4")
        self.assertIsInstance(source, str)

    def test_no_recording_when_output_path_is_none(self):
        sensor = VehicleSensor([], video_path=0, output_path=None)
        self.assertIsNone(sensor.output_path)

    @unittest.skipUnless(importlib.util.find_spec("cv2"), "opencv not installed")
    def test_missing_webcam_stops_start_with_clear_error(self):
        sensor = VehicleSensor([], video_path=99, display=False)   # no webcam number 99
        with self.assertRaises(RuntimeError) as context:
            sensor.start()
        self.assertIn("webcam", str(context.exception))


if __name__ == "__main__":
    unittest.main()