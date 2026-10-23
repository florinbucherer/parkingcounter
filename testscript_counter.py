from counter import PCounter
from sensor import Direction

IN = Direction.IN    # car comes in
OUT = Direction.OUT  # car goes out


def check(name, counter, expected_free):
    ok = counter.free == expected_free
    print(f"{'PASS' if ok else 'FAIL'}  {name}: free spaces = {counter.free}")
    assert ok, f"expected {expected_free}"


# empty lot
c = PCounter(10)
check("empty lot", c, 10)

# one car in
c.apply(IN)
check("one car in", c, 9)

# one car out
c.apply(OUT)
check("one car out", c, 10)

# fill the lot, then try to add more
c = PCounter(2)
c.apply(IN)
c.apply(IN)
check("lot full", c, 0)
c.apply(IN)
check("extra car (stays full)", c, 0)

# das Auto ohne Platz fährt wieder raus -> es darf kein Platz frei werden
c.apply(OUT)
check("extra car leaves again (still full)", c, 0)

# erst wenn ein Auto rausfährt, das wirklich geparkt hat, wird ein Platz frei
c.apply(OUT)
check("parked car leaves (1 space free)", c, 1)

# more cars leaving than entered
c = PCounter(3)
c.apply(OUT)
check("car out of empty lot", c, 3)

# start with some cars already inside
c = PCounter(10, 4)
check("start with 4 cars", c, 6)

# change capacity
c.set_capacity(20)
check("capacity changed to 20", c, 16)

print("\nAll tests passed.")