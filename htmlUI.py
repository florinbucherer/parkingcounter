import time
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from ui_interface import IUI

# Read the file index.html (it lies in the same folder as this file)
PAGE = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

# Here we store the numbers. They are normal variables outside of the classes,
# so that both the handler and the class WebUI can use them. This solves the problem how to share values between the two classes.
total = 0               # all parking lots
occupied_at_start = 0   # parking lots that are already occupied at the start
free = 0                # free parking lots (updated all the time)
configured = False      # becomes True as soon as the user has submitted the settings
exit_requested = False  # becomes True when the user presses the exit button


# The handler answers the requests from the browser.
# do_GET is called automatically whenever the browser opens an address.
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global total, occupied_at_start, free, configured, exit_requested   # we want to change these global variables

        if self.path.startswith("/set"):
            # When The browser sent the settings, e.g. "/set/50/10"
            parts = self.path.split("/")        # split them and store them in a list: ["", "set", "50", "10"]
            try:
                new_total = int(parts[2])       # 50
                new_occupied = int(parts[3])    # 10
            except (IndexError, ValueError):    # e.g. "/set//" when an input field was empty
                new_total, new_occupied = 0, -1
            if new_total < 1 or not 0 <= new_occupied <= new_total:
                self.send_error(400, "Invalid settings")   # answer with an error instead of crashing the handler
                return
            if not configured:                  # the settings can only be sent once, otherwise the page and the counter would disagree
                total = new_total
                occupied_at_start = new_occupied
                free = total - occupied_at_start
                configured = True
            text = ""                           # the browser does not need an answer

        elif self.path == "/exit":
            # The exit button was pressed: main.py will notice this in show() and end the program
            exit_requested = True
            text = ""

        elif self.path == "/status":
            # when the web page asks for the current number from the main eg. from parkingcounter
            if configured:
                text = str(free) + " / " + str(total)
            else:
                text = ""                       # empty because nothing set yet

        else:
            # Everything else (normally "/"): send the web page itself
            text = PAGE

        # Send the answer to the browser
        self.send_response(200) #statuscode -> everything okay
        self.send_header("Content-Type", "text/html; charset=utf-8") #set the content type to HTML
        self.end_headers() #end header to let the browser know that now the actual content follows
        self.wfile.write(text.encode()) #send the actual content from the variable text to the browser

    def log_message(self, format, *args):
        pass   # the page asks /status every 0.5 s, do not print every request to the console


class WebUI(IUI):
    _server = None

    def start(self):
        # Start the web server in its own thread so the program does not get stuck.
        # 127.0.0.1 = only this computer may connect (0.0.0.0 would let everybody in the network press Exit).
        self._server = HTTPServer(("127.0.0.1", 8000), Handler)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()

        # Open the browser
        webbrowser.open("http://localhost:8000")

        # Wait until the user has submitted the settings
        while not configured:
            time.sleep(0.1)

        # Write the numbers into the dictionary of the counter (main gave it to us), the counter owns them
        self.values["capacity"] = total
        self.values["occupied"] = occupied_at_start

    def show(self, occupied, free_now):
        global free, total
        free = free_now   # just remember it, the browser fetches the number itself
        total = self.values["capacity"]   # another UI may have changed the capacity, so the page must follow
        if exit_requested:
            self.running = False   # main.py stops its loop, then stops the sensor and the UI

    def stop(self):
        if self._server is not None:   # release port 8000
            self._server.shutdown()
            self._server.server_close()
            self._server = None