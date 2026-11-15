import unittest

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


if __name__ == "__main__":
    unittest.main()
