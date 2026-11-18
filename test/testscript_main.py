import unittest
from unittest.mock import MagicMock, patch

import main
from sensor_interface import Direction


class TestMain(unittest.TestCase):

    def make_ui(self, capacity=10, occupied=0):
        ui = MagicMock()
        # like a real UI: at start it writes the numbers of the user into the dictionary that main gave it
        ui.start.side_effect = lambda: ui.values.update(capacity=capacity, occupied=occupied)
        ui.running = True
        return ui

    @staticmethod
    def ui_class(ui):
        """Replacement for the class WebUI: like the real one it keeps the dictionary it is given."""
        def create(values):
            ui.values = values
            return ui
        return create

    def run_main(self, ui, sensor):
        # replace the real classes and the waiting time
        with patch("main.WebUI", side_effect=self.ui_class(ui)), \
             patch("main.LogUI"), \
             patch("main.VehicleSensor", return_value=sensor) as sensor_class, \
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

        with patch("main.WebUI", side_effect=self.ui_class(ui)), \
             patch("main.LogUI"), \
             patch("main.VehicleSensor", side_effect=make_sensor), \
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
                ui.values["capacity"] = 20     # user changes the capacity in the UI
            else:
                ui.running = False

        ui.show.side_effect = show
        self.run_main(ui, sensor)
        self.assertEqual(shown, [10, 20])

    def test_counter_values_are_given_to_every_ui(self):
        ui = self.make_ui(capacity=10, occupied=3)
        sensor = MagicMock()
        ui.show.side_effect = lambda occupied, free: setattr(ui, "running", False)
        with patch("main.WebUI", side_effect=self.ui_class(ui)), \
             patch("main.LogUI") as log_class, \
             patch("main.VehicleSensor", return_value=sensor), \
             patch("main.time.sleep"):
            main.main()
        # both UIs got the same dictionary when they were created, so the numbers of the main UI are also in the log UI
        log_values = log_class.call_args.args[0]
        self.assertIs(log_values, ui.values)
        self.assertEqual(log_values, {"capacity": 10, "occupied": 3})

    def test_second_ui_can_change_capacity(self):
        ui = self.make_ui(capacity=10)
        sensor = MagicMock()
        shown = []

        def show(occupied, free):
            shown.append(free)
            if len(shown) == 1:
                log_class.call_args.args[0]["capacity"] = 30   # changed in the second UI
            else:
                ui.running = False

        ui.show.side_effect = show
        with patch("main.WebUI", side_effect=self.ui_class(ui)), \
             patch("main.LogUI") as log_class, \
             patch("main.VehicleSensor", return_value=sensor), \
             patch("main.time.sleep"):
            main.main()
        self.assertEqual(shown, [10, 30])

    def test_ctrl_c_still_cleans_up(self):
        ui = self.make_ui()
        sensor = MagicMock()
        ui.show.side_effect = KeyboardInterrupt
        self.run_main(ui, sensor)
        sensor.stop.assert_called_once()
        ui.stop.assert_called_once()