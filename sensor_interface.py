from abc import ABC, abstractmethod
from enum import Enum


class Direction(Enum):
    IN = 1
    OUT = -1


class ISensor(ABC):
    """Interface (superclass) for every sensor.

    A sensor appends a Direction event to the list it is given
    whenever a car passes. How it detects the car is its own business.
    """

    def __init__(self, events: list):
        self.events = events

    @abstractmethod
    def start(self):
        """Start detecting. Must return immediately (run a thread inside if needed)."""

    @abstractmethod
    def stop(self):
        """Stop detecting and clean up."""
