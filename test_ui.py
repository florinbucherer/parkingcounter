import threading

from ui import UI


class ConsoleUI(UI):
    """Prints the result to the console.

    At start it asks for the capacity and for the cars already inside.
    Afterwards: type a number (e.g. 60) and press Enter to change the
    capacity, or type q to quit the program.
    """

    def __init__(self, capacity: int = 50, start_occupied: int = 0):
        super().__init__(capacity, start_occupied)
        self._last = None

    def start(self):
        self.capacity = self._ask("Number of parking spaces", self.capacity, minimum=1)
        self.start_occupied = self._ask(
            "Spaces already occupied",
            min(self.start_occupied, self.capacity),
            minimum=0,
            maximum=self.capacity,
        )
        print("Type a number to change the capacity, or q to quit.")
        threading.Thread(target=self._read_input, daemon=True).start()

    def _ask(self, prompt: str, default: int, minimum: int, maximum: int = None) -> int:
        """Ask until a valid whole number is entered. Enter alone keeps the default."""
        while True:
            try:
                text = input(f"{prompt} [{default}]: ").strip()
            except EOFError:
                return default           # no input possible: keep the default
            if text == "":
                return default
            value = self._parse(text, minimum)
            if value is not None and (maximum is None or value <= maximum):
                return value
            if maximum is None:
                print(f"Please enter a whole number of at least {minimum}.")
            else:
                print(f"Please enter a whole number from {minimum} to {maximum}.")

    @staticmethod
    def _parse(text: str, minimum: int):
        """Return the number as int, or None if it is not a whole number >= minimum."""
        try:
            value = int(text)
        except ValueError:
            return None
        return value if value >= minimum else None

    def show(self, occupied: int, free: int):
        state = (occupied, free, self.capacity)
        if state == self._last:          # only print when something changed
            return
        self._last = state
        full = "  -> FULL" if free == 0 else ""
        print(f"Free: {free:3d} | Occupied: {occupied:3d} / {self.capacity}{full}")

    def _read_input(self):
        while True:
            try:
                text = input()
            except EOFError:
                return
            if text.strip().lower() in ("q", "quit", "exit"):
                self.running = False
                return
            value = self._parse(text, 1)
            if value is None:
                print("Please enter a positive whole number, or q to quit.")
            else:
                self.capacity = value