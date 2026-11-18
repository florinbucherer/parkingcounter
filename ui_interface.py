from abc import ABC, abstractmethod


class IUI(ABC):
    """Interface (superclass) for every user interface.

    The UI does not own any numbers. The counter owns capacity and occupied in a
    dictionary, and main hands this dictionary to every UI when it creates it,
    e.g. WebUI(counter.values). So all UIs work on the same numbers:
        self.values["capacity"]   total number of parking lots
        self.values["occupied"]   occupied parking lots (set it in start() if the user
                                  enters how many are already occupied at program start)
    Main passes occupied/free to show(). A concrete UI may change
    self.values["capacity"] whenever the user asks for it.
    """

    def __init__(self, values: dict):
        # The dictionary of the counter. It is required on purpose: a UI that forgets to pass it
        # on to super().__init__(values) fails at once and does not silently work on empty numbers.
        self.values = values
        self.running = True

    @abstractmethod
    def start(self):
        """
        Start the UI. Must return immediately (run a thread inside if needed).
        Optionally ask user for how many parking lots are already occupied at program start and set self.values["occupied"] accordingly.
        """
        self.values["capacity"] = int(input("Capacity of the parking lot : "))

    @abstractmethod
    def show(self, occupied: int, free: int):
        print(f"Occupied : {occupied} | Free : {free}")
        """Display the current numbers."""

    def stop(self):
        """Optional: clean up. Does nothing by default."""