import threading
import unittest
import urllib.request
from http.server import HTTPServer
from unittest.mock import patch

import htmlUI
from htmlUI import Handler, WebUI


def reset_numbers():
    """Put the shared variables back to the start values."""
    htmlUI.total = 0
    htmlUI.occupied_at_start = 0
    htmlUI.free = 0
    htmlUI.configured = False


class TestHandler(unittest.TestCase):

    def setUp(self):
        reset_numbers()
        # real server on a free port (0 = the system picks one)
        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        reset_numbers()

    def get(self, path):
        with urllib.request.urlopen(f"http://127.0.0.1:{self.port}{path}") as answer:
            return answer.status, answer.read().decode()

    def test_main_page(self):
        status, text = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("Settings", text)

    def test_status_empty_before_settings(self):
        status, text = self.get("/status")
        self.assertEqual(status, 200)
        self.assertEqual(text, "")

    def test_set_stores_numbers(self):
        self.get("/set/50/10")
        self.assertEqual(htmlUI.total, 50)
        self.assertEqual(htmlUI.occupied_at_start, 10)
        self.assertEqual(htmlUI.free, 40)
        self.assertTrue(htmlUI.configured)

    def test_status_after_settings(self):
        self.get("/set/50/10")
        _, text = self.get("/status")
        self.assertEqual(text, "40 / 50")

    def test_status_follows_free_number(self):
        self.get("/set/50/10")
        htmlUI.free = 12
        _, text = self.get("/status")
        self.assertEqual(text, "12 / 50")


class TestWebUI(unittest.TestCase):

    def setUp(self):
        reset_numbers()

    def tearDown(self):
        reset_numbers()

    def test_start_takes_over_the_settings(self):
        htmlUI.total = 30
        htmlUI.occupied_at_start = 5
        htmlUI.configured = True   # as if the user pressed Start
        ui = WebUI()
        # no real server and no real browser
        with patch("htmlUI.HTTPServer"), patch("htmlUI.threading.Thread"), patch("htmlUI.webbrowser.open") as browser:
            ui.start()
        browser.assert_called_once_with("http://localhost:8000")
        self.assertEqual(ui.capacity, 30)
        self.assertEqual(ui.start_occupied, 5)

    def test_show_remembers_free_number(self):
        WebUI().show(10, 15)
        self.assertEqual(htmlUI.free, 15)
