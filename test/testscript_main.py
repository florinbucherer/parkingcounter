import unittest
from unittest.mock import MagicMock, patch

import main
from sensor_interface import Direction


class TestMain(unittest.TestCase):

    def make_ui(self, capacity=10, occupied=0):
        ui = MagicMock()
        ui.capacity = capacity
        ui.start_occupied = occupied
        ui.running = True
        return ui

    def run_main(self, ui, sensor):
        # replace the real classes and the waiting time
        with patch("main.WebUI", return_value=ui), \
             patch("main.FakeSensor", return_value=sensor) as sensor_class, \
             patch("main.time.sleep"):
            main.main()
        return sensor_class

    def test_start_and_stop(self):
        ui = self.make_ui()
        sensor = MagicMock()
        ui.show.side_effect = lambda occupied, free: setattr(ui, "running", False)
        self.run_main(ui, sensor)
        ui.start.assert_called_once()
        sensor.start.assert_called_once()
        sensor.stop.assert_called_once()
        ui.stop.assert_called_once()

    def test_events_are_counted(self):
        ui = self.make_ui(capacity=10, occupied=2)
        shown = []

        def show(occupied, free):
            shown.append((occupied, free))
            ui.running = False

        ui.show.side_effect = show

        # fake sensor: when started it puts two cars in and one out
        def make_sensor(events):
            sensor = MagicMock()
            sensor.start.side_effect = lambda: events.extend([Direction.IN, Direction.IN, Direction.OUT])
            return sensor

        with patch("main.WebUI", return_value=ui), \
             patch("main.FakeSensor", side_effect=make_sensor), \
             patch("main.time.sleep"):
            main.main()
        self.assertEqual(shown, [(3, 7)])   # 2 + 2 - 1 = 3 occupied

    def test_capacity_change_reaches_counter(self):
        ui = self.make_ui(capacity=10)
        sensor = MagicMock()
        shown = []

        def show(occupied, free):
            shown.append(free)
            if len(shown) == 1:
                ui.capacity = 20     # user changes the capacity
            else:
                ui.running = False

        ui.show.side_effect = show
        self.run_main(ui, sensor)
        self.assertEqual(shown, [10, 20])

    def test_ctrl_c_still_cleans_up(self):
        ui = self.make_ui()
        sensor = MagicMock()
        ui.show.side_effect = KeyboardInterrupt
        self.run_main(ui, sensor)
        sensor.stop.assert_called_once()
        ui.stop.assert_called_once()
