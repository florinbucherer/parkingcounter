import unittest
from unittest.mock import patch

from sensor import Sensor
from sensor_interface import ISensor, Direction


class TestISensor(unittest.TestCase):

    def test_interface_cannot_be_created(self):
        # abstract class: start() and stop() are missing
        with self.assertRaises(TypeError):
            ISensor([])

    def test_direction_values(self):
        self.assertEqual(Direction.IN.value, 1)
        self.assertEqual(Direction.OUT.value, -1)


class TestSensor(unittest.TestCase):

    def test_keeps_event_list(self):
        events = []
        s = Sensor(events)
        self.assertIs(s.events, events)

    def test_loop_adds_one_event(self):
        events = []
        s = Sensor(events)
        s._running.set()
        # the fake sleep stops the loop after the first round
        with patch("sensor.time.sleep", side_effect=lambda t: s._running.clear()):
            s._loop()
        self.assertEqual(len(events), 1)
        self.assertIn(events[0], (Direction.IN, Direction.OUT))

    def test_loop_does_nothing_when_stopped(self):
        events = []
        s = Sensor(events)
        s._loop()   # running flag is not set
        self.assertEqual(events, [])

    def test_start_and_stop(self):
        s = Sensor([])
        with patch("sensor.time.sleep"):   # no waiting
            s.start()
            self.assertTrue(s._running.is_set())
            s.stop()
        self.assertFalse(s._running.is_set())
        self.assertFalse(s._thread.is_alive())

    def test_stop_without_start(self):
        s = Sensor([])
        s.stop()   # must not crash
        self.assertFalse(s._running.is_set())
