import time

from test_sensor import FakeSensor        # Test sensor: swap for real sensor
from test_ui import ConsoleUI          # Test UI: swap for real UI
from counter import PCounter


def main():
    events = []                           # shared list to queue events like car in or car out: sensor appends, main removes

    ui = ConsoleUI()                      # test UI: swap for real UI
    sensor = FakeSensor(events)           # test sensor: swap for real sensor
    ui.start()
    sensor.start()
    counter = PCounter(ui.capacity, ui.start_occupied)  # counter knows nothing about sensors or UI, it just counts the cars in and out

    try:
        while ui.running:   #while the UI is running, this can be stopped by the UI itself.
            while events:   #while events is not empty, pop the first event and apply it to the counter
                counter.apply(events.pop(0))
            counter.set_capacity(ui.capacity)  # update capacity of the UI in counter.
            ui.show(counter.occupied, counter.free)
            time.sleep(0.1)
    except KeyboardInterrupt:   #exit program on Ctrl+C
        pass
    finally:    #this runs in both cases, it cleans up and stops sensor and ui. This is important for the case that threads are used that must be cleaned up.
        sensor.stop()
        ui.stop()


if __name__ == "__main__":
    main()