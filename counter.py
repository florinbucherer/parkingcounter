from sensor_interface import Direction


class PCounter:
    """The counter owns the numbers and knows nothing about sensors or UI.

    The numbers (capacity and occupied) live in the dictionary self.values.
    Main hands this one dictionary to every UI, so all UIs show and change the
    same numbers (e.g. the user enters the start values or a new capacity).
    """

    def __init__(self, capacity: int = 50, occupied: int = 0):
        self.values = {"capacity": capacity, "occupied": max(0, occupied)}

    @property
    def capacity(self) -> int:
        return self.values["capacity"]

    @capacity.setter
    def capacity(self, capacity: int):
        self.values["capacity"] = capacity

    @property
    def occupied(self) -> int:
        return self.values["occupied"]

    @occupied.setter
    def occupied(self, occupied: int):
        self.values["occupied"] = max(0, occupied)

    def apply(self, direction: Direction):
        self.occupied = self.occupied + direction.value   # the setter keeps it from going below 0

    @property
    def free(self) -> int:
        return max(0, self.capacity - self.occupied)