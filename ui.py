from abc import ABC, abstractmethod


class UI(ABC):
    """Interface (superclass) for every user interface.

    The UI shows the result and owns the capacity setting.
    Main reads ui.capacity and passes occupied/free to show().
    A concrete UI may change self.capacity whenever the user asks for it.
    """

    def __init__(self, capacity: int = 50):
        self.capacity = capacity

    @abstractmethod
    def start(self):
        """Start the UI. Must return immediately (run a thread inside if needed)."""

    @abstractmethod
    def show(self, occupied: int, free: int):
        """Display the current numbers."""

    def stop(self):
        """Optional: clean up. Does nothing by default."""
