import json
import re
import shutil
import subprocess
import unittest

import htmlUI

# The page (index.html) as the browser gets it
PAGE = htmlUI.PAGE


def active_page():
    """The page without the comments, so only the code that really runs is left."""
    text = re.sub(r"<!--.*?-->", "", PAGE, flags=re.S)    # html comments
    return re.sub(r"/\*.*?\*/", "", text, flags=re.S)     # css and javascript comments


class TestPageStructure(unittest.TestCase):

    def setUp(self):
        self.page = active_page()

    def test_script_only_uses_existing_ids(self):
        ids_in_page = set(re.findall(r'id="([^"]+)"', self.page))
        ids_in_script = set(re.findall(r'getElementById\("([^"]+)"\)', self.page))
        self.assertTrue(ids_in_script)                       # the script uses some ids
        self.assertEqual(ids_in_script - ids_in_page, set())   # and all of them are in the page

    def test_page_fits_on_a_phone(self):
        self.assertIn('name="viewport"', self.page)

    def test_page_asks_the_server_routes(self):
        for route in ('"/set/"', '"/status"', '"/exit"'):
            self.assertIn(route, self.page)

    def test_status_text_is_split_like_the_server_sends_it(self):
        self.assertIn('split(" / ")', self.page)             # the server sends "free / total"

    def test_buttons_call_existing_functions(self):
        for function in ("save", "exitApp"):
            self.assertIn(f'onclick="{function}()"', self.page)
            self.assertIn(f"function {function}(", self.page)

    def test_start_and_exit_views_exist(self):
        for text in ("Settings", "Free parking lots", "Occupancy", "Program ended"):
            self.assertIn(text, self.page)

    def test_statistics_are_commented_out(self):
        self.assertNotIn("showStats", self.page)             # not active
        self.assertNotIn('id="stats"', self.page)
        self.assertIn("showStats", PAGE)                     # but still in the file as a comment




