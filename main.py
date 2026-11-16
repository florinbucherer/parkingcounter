import time

from vehicle_sensor import VehicleSensor
from htmlUI import WebUI                   # Import UI
from logui import LogUI                   # Import second UI (log file)
from counter import PCounter


def main():
    events = []                           # shared list to queue events like car in or car out: sensor appends, main removes

    UIs = [WebUI(), LogUI("parkingcounter_log.txt")]  # UI's: Main UI must be the first one, when this UI is stopped, the program ends. The second UI is independent and can be added or removed.
    sensor = VehicleSensor(events)         # sensor knows nothing about the UI or the counter, it just detects cars and appends events to the list
    
    for ui in UIs:
        ui.start()
    sensor.start()
    counter = PCounter(ui.capacity, ui.start_occupied)  # counter knows nothing about sensors or UI, it just counts the cars in and out

    try:
        while UIs[0].running:   #while the UI is running, this can be stopped by the UI itself.
            while events:   #while events is not empty, pop the first event and apply it to the counter
                counter.apply(events.pop(0))
            counter.set_capacity(ui.capacity)  # update capacity of the UI in counter.
            for ui in UIs:   #show the current numbers in all UIs, the main UI is the first one, the second UI is independent and can be added or removed.
                ui.show(counter.occupied, counter.free)
            time.sleep(0.1)
    except KeyboardInterrupt:   #exit program on Ctrl+C
        pass
    finally:    #this runs in both cases, it cleans up and stops sensor and ui. This is important for the case that threads are used that must be cleaned up.
        sensor.stop()
        for ui in UIs:
            ui.stop()


if __name__ == "__main__":
    main()