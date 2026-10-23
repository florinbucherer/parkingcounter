from sensor import Direction


class PCounter:
    """The counter knows nothing about sensors or UI."""

    def __init__(self, capacity: int, occupied: int = 0):
        self.capacity = capacity
        self.occupied = max(0, occupied)

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def apply(self, direction: Direction):
        self.occupied = max(0, self.occupied + direction.value)

    @property
    def free(self) -> int:
        return max(0, self.capacity - self.occupied)