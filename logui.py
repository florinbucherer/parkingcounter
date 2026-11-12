from datetime import datetime

from ui_interface import IUI


class LogUI(IUI):
    """Independent second UI: writes every change of the parking lot to a text file.

    It knows nothing about other UIs, the sensor or the counter. It only gets the numbers
    through show() and writes a line directly, no own thread needed because a short line is written very fast.
    The file is given when the instance is created, e.g. LogUI("parkingcounter_log.txt").
    It is added to the program by putting it into the list extra_uis in main.py and removed by taking it out.

    One line per change:  time | event | free lots | occupied lots
    """

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file   # path of the text file, given by the one who creates the LogUI
        self._last = None          # (occupied, free) from the last call of show()

    def start(self):
        pass   # nothing to start, the file is opened whenever a line is written

    def show(self, occupied, free):
        if self._last is None:
            self._log("Start", occupied, free)
        elif occupied > self._last[0]:
            cars = occupied - self._last[0]
            self._log("Car in" if cars == 1 else f"{cars} cars in", occupied, free)
        elif occupied < self._last[0]:
            cars = self._last[0] - occupied
            self._log("Car out" if cars == 1 else f"{cars} cars out", occupied, free)
        self._last = (occupied, free)

    def stop(self):
        if self._last is not None:
            self._log("Stop", *self._last)
            self._last = None

    def _log(self, event, occupied, free):
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as file:   # "a" = append, old lines stay
            file.write(f"{time_now} | {event:<12} | Free: {free:3d} | Occupied: {occupied:3d}\n")