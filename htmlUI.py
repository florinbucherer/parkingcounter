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


# The handler answers the requests from the browser.
# do_GET is called automatically whenever the browser opens an address.
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global total, occupied_at_start, free, configured   # we want to change these global variables

        if self.path.startswith("/set"):
            # When The browser sent the settings, e.g. "/set/50/10"
            parts = self.path.split("/")        # split them and store them in a list: ["", "set", "50", "10"]
            total = int(parts[2])               # 50
            occupied_at_start = int(parts[3])   # 10
            free = total - occupied_at_start
            configured = True
            text = ""                           # the browser does not need an answer

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

class WebUI(IUI):
    def start(self):
        # Start the web server in its own thread so the program does not get stuck
        server = HTTPServer(("0.0.0.0", 8000), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()

        # Open the browser
        webbrowser.open("http://localhost:8000")

        # Wait until the user has submitted the settings
        while not configured:
            time.sleep(0.1)

        # Pass the numbers on to main.py (main.py reads capacity and start_occupied)
        self.capacity = total
        self.start_occupied = occupied_at_start

    def show(self, occupied, free_now):
        global free
        free = free_now   # just remember it, the browser fetches the number itself