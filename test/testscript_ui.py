import io
import unittest
from unittest.mock import patch

from dummy_ui import ConsoleUI
from ui_interface import IUI


class SimpleUI(IUI):
    """Smallest possible UI, only to test the interface."""

    def start(self):
        pass

    def show(self, occupied, free):
        pass


class TestIUI(unittest.TestCase):

    def test_interface_cannot_be_created(self):
        with self.assertRaises(TypeError):
            IUI()

    def test_default_values(self):
        ui = SimpleUI()
        self.assertEqual(ui.capacity, 50)
        self.assertEqual(ui.start_occupied, 0)
        self.assertTrue(ui.running)

    def test_stop_does_nothing(self):
        ui = SimpleUI()
        ui.stop()
        self.assertTrue(ui.running)

    def test_default_start_asks_capacity(self):
        ui = SimpleUI()
        with patch("builtins.input", return_value="30"):
            IUI.start(ui)
        self.assertEqual(ui.capacity, 30)

    def test_default_show_prints_numbers(self):
        ui = SimpleUI()
        with patch("sys.stdout", new=io.StringIO()) as out:
            IUI.show(ui, 3, 7)
        self.assertIn("Occupied : 3", out.getvalue())
        self.assertIn("Free : 7", out.getvalue())


class TestConsoleUIParse(unittest.TestCase):

    def test_valid_number(self):
        self.assertEqual(ConsoleUI._parse("5", 1), 5)

    def test_not_a_number(self):
        self.assertIsNone(ConsoleUI._parse("abc", 1))

    def test_below_minimum(self):
        self.assertIsNone(ConsoleUI._parse("0", 1))

    def test_minimum_is_allowed(self):
        self.assertEqual(ConsoleUI._parse("0", 0), 0)


class TestConsoleUIAsk(unittest.TestCase):

    def setUp(self):
        self.ui = ConsoleUI()

    def ask(self, answers, **kwargs):
        # input() returns the answers one after the other, output is hidden
        with patch("builtins.input", side_effect=answers), patch("sys.stdout", new=io.StringIO()):
            return self.ui._ask("Question", 10, **kwargs)

    def test_enter_keeps_default(self):
        self.assertEqual(self.ask([""], minimum=1), 10)

    def test_valid_number(self):
        self.assertEqual(self.ask(["25"], minimum=1), 25)

    def test_asks_again_after_wrong_input(self):
        self.assertEqual(self.ask(["abc", "-3", "7"], minimum=1), 7)

    def test_asks_again_above_maximum(self):
        self.assertEqual(self.ask(["99", "8"], minimum=0, maximum=10), 8)

    def test_no_input_keeps_default(self):
        self.assertEqual(self.ask(EOFError(), minimum=1), 10)


class TestConsoleUIStart(unittest.TestCase):

    def test_start_sets_values(self):
        ui = ConsoleUI()
        with patch("builtins.input", side_effect=["20", "5"]), \
             patch("sys.stdout", new=io.StringIO()), \
             patch("dummy_ui.threading.Thread") as thread:
            ui.start()
        self.assertEqual(ui.capacity, 20)
        self.assertEqual(ui.start_occupied, 5)
        thread.return_value.start.assert_called_once()   # input thread was started


class TestConsoleUIShow(unittest.TestCase):

    def show(self, ui, occupied, free):
        with patch("sys.stdout", new=io.StringIO()) as out:
            ui.show(occupied, free)
        return out.getvalue()

    def test_show_prints_numbers(self):
        text = self.show(ConsoleUI(10), 4, 6)
        self.assertIn("Free:   6", text)
        self.assertIn("Occupied:   4 / 10", text)
        self.assertNotIn("FULL", text)

    def test_show_full(self):
        text = self.show(ConsoleUI(10), 10, 0)
        self.assertIn("FULL", text)

    def test_same_state_prints_only_once(self):
        ui = ConsoleUI(10)
        self.show(ui, 4, 6)
        self.assertEqual(self.show(ui, 4, 6), "")


class TestConsoleUIReadInput(unittest.TestCase):

    def read(self, ui, lines):
        with patch("builtins.input", side_effect=lines), patch("sys.stdout", new=io.StringIO()) as out:
            ui._read_input()
        return out.getvalue()

    def test_number_changes_capacity(self):
        ui = ConsoleUI(10)
        self.read(ui, ["60", "q"])
        self.assertEqual(ui.capacity, 60)

    def test_q_stops_ui(self):
        ui = ConsoleUI(10)
        self.read(ui, ["q"])
        self.assertFalse(ui.running)

    def test_quit_word_stops_ui(self):
        ui = ConsoleUI(10)
        self.read(ui, ["  QUIT "])
        self.assertFalse(ui.running)

    def test_wrong_input_prints_message(self):
        ui = ConsoleUI(10)
        text = self.read(ui, ["abc", "q"])
        self.assertIn("Please enter a positive whole number", text)
        self.assertEqual(ui.capacity, 10)

    def test_end_of_input_stops_loop(self):
        ui = ConsoleUI(10)
        self.read(ui, EOFError())
        self.assertTrue(ui.running)
