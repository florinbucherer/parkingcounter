import unittest

from counter import PCounter
from sensor_interface import Direction

IN = Direction.IN    # car comes in
OUT = Direction.OUT  # car goes out


class TestPCounter(unittest.TestCase):

    def show(self, name, counter):
        print(f"{name}: free spaces = {counter.free}")

    def test_empty_lot(self):
        c = PCounter(10)
        self.show("empty lot", c)
        self.assertEqual(c.free, 10)

    def test_one_car_in(self):
        c = PCounter(10)
        c.apply(IN)
        self.show("one car in", c)
        self.assertEqual(c.free, 9)

    def test_one_car_out(self):
        c = PCounter(10, 1)
        c.apply(OUT)
        self.show("one car out", c)
        self.assertEqual(c.free, 10)

    def test_lot_full(self):
        c = PCounter(2)
        c.apply(IN)
        c.apply(IN)
        self.show("lot full", c)
        self.assertEqual(c.free, 0)

    def test_extra_car_stays_full(self):
        c = PCounter(2)
        c.apply(IN)
        c.apply(IN)
        c.apply(IN)  # no space left
        self.show("extra car", c)
        self.assertEqual(c.free, 0)

    def test_extra_car_leaves_again(self):
        c = PCounter(2)
        c.apply(IN)
        c.apply(IN)
        c.apply(IN)   # car finds no space
        c.apply(OUT)  # and drives out again
        self.show("extra car leaves again", c)
        self.assertEqual(c.free, 0)

    def test_parked_car_leaves(self):
        c = PCounter(2)
        c.apply(IN)
        c.apply(IN)
        c.apply(IN)   # extra car
        c.apply(OUT)  # extra car leaves
        c.apply(OUT)  # parked car leaves
        self.show("parked car leaves", c)
        self.assertEqual(c.free, 1)

    def test_car_out_of_empty_lot(self):
        c = PCounter(3)
        c.apply(OUT)
        self.show("car out of empty lot", c)
        self.assertEqual(c.free, 3)

    def test_start_with_cars(self):
        c = PCounter(10, 4)
        self.show("start with 4 cars", c)
        self.assertEqual(c.free, 6)

    def test_change_capacity(self):
        c = PCounter(10, 4)
        c.capacity = 20
        self.show("capacity changed to 20", c)
        self.assertEqual(c.free, 16)

    def test_counter_owns_the_values_in_a_dictionary(self):
        c = PCounter(10, 4)
        self.assertEqual(c.values, {"capacity": 10, "occupied": 4})

    def test_default_values(self):
        c = PCounter()
        self.assertEqual(c.values, {"capacity": 50, "occupied": 0})

    def test_change_in_dictionary_reaches_counter(self):
        # a UI writes into the dictionary that main gave it
        c = PCounter(10, 4)
        c.values["capacity"] = 30
        c.values["occupied"] = 6
        self.show("dictionary changed by a UI", c)
        self.assertEqual(c.free, 24)

    def test_cars_are_visible_in_dictionary(self):
        # the UIs see the cars without asking the counter
        c = PCounter(10, 4)
        c.apply(IN)
        self.assertEqual(c.values["occupied"], 5)

    def test_start_occupied_is_never_negative(self):
        c = PCounter(10, -3)
        self.assertEqual(c.values["occupied"], 0)