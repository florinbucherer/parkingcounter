import random
import threading
import time

from sensor import Sensor, Direction


class FakeSensor(Sensor):
    """Emits random IN/OUT events. For developing without a camera."""

    def __init__(self, events: list):
        super().__init__(events)
        self._running = threading.Event()
        self._thread = None

    def start(self):
        self._running.set()
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running.clear()
        if self._thread:
            self._thread.join()

    def _loop(self):
        while self._running.is_set():
            time.sleep(random.uniform(0.5, 2.0))
            self.events.append(random.choice([Direction.IN, Direction.OUT]))
