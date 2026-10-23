from abc import ABC, abstractmethod


class IUI(ABC):
    """Interface (superclass) for every user interface.

    The UI shows the result and owns the capacity setting.
    Main reads ui.capacity and passes occupied/free to show().
    A concrete UI may change self.capacity whenever the user asks for it.
    """

    def __init__(self, capacity: int = 50, start_occupied: int = 0):
        self.capacity = capacity
        self.start_occupied = start_occupied   # cars already inside at program start
        self.running = True

    @abstractmethod
    def start(self):
        """
        Start the UI. Must return immediately (run a thread inside if needed).
        Optionally ask user for how many parking lots are already occupied at program start and set self.start_occupied accordingly.
        """

    @abstractmethod
    def show(self, occupied: int, free: int):
        """Display the current numbers."""

    def stop(self):
        """Optional: clean up. Does nothing by default."""
