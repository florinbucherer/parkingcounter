# ToDo
- Description from which Side must Camera be pointed.
- Description User Guide how long to wait until program works at startup
- Explanation of Abstraction
- Explanation of why simple (What features could be added)
- Why lists instead of qeues
- Why abstract classes instead of Interfaces
# Project Documentation: ParkingCounter

## 1. Introduction, Objectives, Constraints
### 1.1 Introduction
ParkingCounter is a program that uses a webcam to monitor the entrance of a parking area. It detects vehicles entering and leaving the parking area, keeps track of occupied and available spaces and displays the current number of available parking lots through an interface. The System is developed for the specific Parking Area above the DHBW-Lörrach and is designed as the Camera would be mounted on the roof of building D facing the street that enters the Parking Area. The Programm could be used for other similar situations too, however when the camera is installed on the other side of the street or the Parking Area is on the other side, the code must be changed accordingly so the programm knows in which direction cars are entering or exiting the Area. As we assume a fix installed installation we did not implement a setting to change the direction.

### 1.2 Objectives
The main goal is to create a working prototype (MVP) that:
-   Monitors the entrance of a parking area using a **webcam**.
-   Detects vehicles entering and leaving the parking area in real time.
-   Counts the number of occupied and free parking spaces across the entire parking Area.
-   Displays the current number of available parking spaces via a **User Interface**.
-   Provides data for later evaluation.

| Basic Requirements | Performance Requirements | Enthusiastic Requirements |
| --- | --- | --- |
| User interface (clear, readable, real-time display) | Car park statistics (occupancy rate by the hour, 24/7 statistics) | Intelligent detection (vehicle type) |
| Count the number of parking spaces available (automatic update, error-proofing) | System performance (update <1s, low error rate) | User guidance (available car parks, mobile app) |
| Camera detection (input/output, reliability) | | Optimisation (predictions, alerts) |

### 1.3 MVP (Minimum Viable Product)
-   **Control unit:** A computer that can run Python
-   **Sensors:** A Webcam
-   **Output:** User Interface
-   **Software:** Python script using an image detection library.
*   **Control unit:** A computer that can run Python
*   **Sensors:** A Webcam
*   **Output:** User Interface
*   **Software:** Python script using a image detection library.
The Product should fullfill as a minimum the Basic Requirements.

### 1.4 Constraints
-   Programming language: **Python**.
-   Version control: **GitHub**.
-   Development model: **Scrum** (3 sprints).

---

## 2. Build Instructions
To set up the project locally, follow these steps:
1.  **Clone the repository:** `git clone https://github.com/florinbucherer/parkingcounter`
2.  **Create a virtual environment:** `python -m venv venv`
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Start the application:** `python main.py`
5.  **Position the camera on the correct side of the road and point it towards the street. For the Parking Area of DHBW Lörrach mount it on the roof of Building D facing the street.**
6.  **Open the UI on a device in the same Network by typing the IP-Adress of the Host Computer followed by :800 into the browser**
7.  **Enjoy :)**

---

## 3. Brief User Guide
1.  Start the Programm (The User Interface will open Autmatically)
2.  Enter number of Parking lots and number of already occupied parking lots at start and press start.
3.  **Position the camera on the correct side of the road and point it towards the street. For the Parking Area of DHBW Lörrach mount it on the roof of Building D facing the street.**
4.  **Open the UI on a device in the same Network by typing the IP-Adress of the Host Computer followed by :800 into the browser**
5.  **Enjoy :)**

---

## 4. Release Plan with Expansion Stages
-   **Release 0.1 (Sprint 0):**
    - Hardware setup,
    - Project structure on GitHub,
    - HelloWorld,
    - Clean Management setup (requirements, priorities, timeline).

-   **Release 0.2 (Sprint 1 - MVP):**
    - Building the Project base (interfaces),
    - Starting the construction of the backend of the User Interface,
    - Building a Counter,
    - Developing a car recognition system that can tell if a car is going in or out of the parking lot.
    
-   **Release 1.0 (Sprint 2):**
    - Develop the CSS code for the UI,
    - New feature: Stats on the occupation of the parking lot,
    - Testing the software.

---

## 5. User Stories (Product Backlog)
Requirements are described in the form of user stories with acceptance criteria, estimated effort, and priority:

| ID | User Story | Acceptance Criterion | Effort (SP) | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **US0** | As a product owner, I want to set up the project initially (GitHub repository, Jira project, release plan, Hello World), so the team can start development efficiently. | Repository and Jira project are created, all team members have access, the repository is cloned locally, and a “Hello World” runs on every computer. | 5 | Highest |
| **US1** | As a Product Owner, I want to set requirements, to plan the project. | Clear requirements are defined, documented, and prioritized in the backlog. | 3 | High |
| **US2** | As a Scrum Master, I want to set priorities for the project to work well. | User stories are prioritized and distributed clearly across the 3 sprints. | 3 | Medium |
| **US3** | As a Scrum Master, I want to do a clear timeline, to have an organized project. | Timeline, milestones, and sprint deadlines are defined and visible to the team. | 3 | Medium |
| **US4** | As a coder, I want to connect the counter to the car recognition system, for it to be able to count with a digital camera and other systems. | Signal output from the recognition system increments/decrements the counter accurately. | 5 | High |
| **US5** | As a User, I want to have a working and accessible UI everywhere and on Phone or PC, that is able to show me in real time if a parking space is free. | The UI displays real-time available space updates across test devices. | 5 | Highest |
| **US6** | As a coder, I want to have a working car recognition system, that can detect if a car goes into the parking lot or goes out. | A functional vision-based detection model is identified and tested for direction tracking. | 8 | Highest |
| **US7** | As a coder, I want to build a working counter, that can count how many cars go in and out the parking lot so that it can be sent to the UI. | The counter updates space counts dynamically and exposes an interface for UI consumption. | 8 | Highest |
| **US8** | As a coder, I want to have a clean documentation for the project to be legible and simple to modify. | Code functions are commented inline and README documentation is complete. | 3 | High |
| **US9** | As a User, I want to be able to trust the recognition program, so that the counter can be trusted. | Detection error rate is quantified and kept within acceptable bounds (<10% error). | 5 | Medium |
| **US10** | As a User, I want to have additional data on the parking situation in the parking lot (stats). | Historical occupancy trends/stats are recorded and rendered visually. | 5 | Medium |
| **US11** | As a User, I want to have a good looking and simple interface, to save some time. | The UI has a clear design and the free parking spaces are easy to read at a glance. | TBD | Low |
| **US12** | As a coder, I want to build an easy to modify UI, so that I can adapt it to every device and every use. | The UI works on phone and PC and can be changed without rewriting the program. | 7 | High |
| **US13** | As a coder, I want to adapt the recognition system for it to work with our program. | The vehicle sensor runs the detection in its own thread and sends the IN/OUT events to the counter, with a video file or a webcam. | 9 | High |

---

## 6. Sprint 0 Documentation (Preparation & Setup)
Sprint 0 focused on creating the organizational and technical foundation for developing the parking space occupancy detector as well as establishing **Clean Management** (requirements, priorities, and project timeline). also Building a Jira space and setting Up the github repository.

### 6.1 User Stories & Task Lists

**User Story US0:** *"As a product owner, I want to set up the project initially (GitHub repository, Jira project, release plan, Hello World), so the team can start development efficiently."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 0.1 | Create the Jira Project for backlog management and sprint control. | 2.0 |
| Task 0.2 | Create the GitHub Repository and invite collaborators. | 1.5 |
| Task 0.3 | Save/clone the GitHub Repository on each PC. | 2.0 |
| Task 0.4 | Execute "Hello World" script on each PC to verify local development setup. | 1.5 |
| Task 0.5 | Create the first release plan (timeline and expansion stages). | 1.5 |
| Task 0.6 | Documentation: create initial chapters in README.md. | 2.5 |

**User Story US1:** *"As a Product Owner, I want to set requirements, to plan the project."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 0.7 | Find the requirements for the project. | 2.5 |
| Task 0.8 | Arrange the requirements, set the priorities for each one. | 2.0 |

**User Story US2:** *"As a Scrum Master, I want to set priorities for the project to work well."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 0.9 | Set priorities for each User Story, arrange it in the 3 Sprints. | 2.0 |

**User Story US3:** *"As a Scrum Master, I want to do a clear timeline, to have an organized project."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 0.10 | Set the timeline and deadlines for each of the Stories and tasks and organize them in the sprint. | 2.5 |

### Results of Sprint 0
-   **Release plan:** Creation of an initial timeline and definition of the expansion stages.
-   **Documentation foundation:** The Documentation is created on Github as readme.md and initial structure is added to fill out later.
-   **Technical framework:** Decision which image recognition library to use.
-   **Documentation:** Fill the first chapters in Readme.md.

---

## 7. Sprint 1 Core Development (MVP Implementation)
In this sprint, a working UI, Counter, Recognition system was coded. they were also connected together. 

### 7.1 User Stories & Task Lists (Estimation in Hours)

**User Story US4:** *"As a coder, I want to connect the counter to the car recognition system, for it to be able to count with a digital camera and other systems."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 1.1 | Build an output from the recognition system to the counter. | 1.0 |
| Task 1.2 | Create a Main program that runs the sensor and the UI and the counter and gives the values to the counter and the UI. | 1.0 |
| Task 1.3 | Add interfaces (superclasses) for the sensor (camera) and the UI to set standards so they are exchangeable and communication between Main and the components works well. | 1.0 |
| Task 1.4 | Build dummy testscripts for Sensor and UI to test the Main Program alone and adapt Main if necessary. | 1.0 |
| Task 1.5 | Test Main script together with actual camera and UI. | 1.0 |

**User Story US5:** *"As a User, I want to have a working and accessible UI everywhere and on Phone or PC, that is able to show me in real time if a parking space is free."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 1.6 | Create the input interface from the counter to the UI. | 2.0 |
| Task 1.7 | Build the UI base. | 2.5 |
| Task 1.8 | Analyse the input from the counter to update the amount of free parking spaces. | 1.0 |

**User Story US6:** *"As a coder, I want to have a working car recognition system, that can detect if a car goes into the parking lot or goes out."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 1.9 | Build the car recognition system. | 4.0 |
| Task 1.10 | Test the recognition system alone, to see how it works. | 1.0 |
| Task 1.11 | Create the Output to the Counter. | 1.0 |

**User Story US7:** *"As a coder, I want to build a working counter, that can count how many cars go in and out the parking lot so that it can be sent to the UI."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 1.12 | Analyse the input signal from the recognition system to the counter, to either add one free parking space or delete one. | 4.0 |
| Task 1.13 | Create the input interface from the counter to the UI. | 2.0 |
| Task 1.14 | Build the central system that connects the counter to everything with a class. | 3.0 |

---

### 7.2 Key Code Snippets
```python
# Counter core class updating free space counts dynamically
class ParkingCounter:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.occupied = 0

    def register_entry(self):
        if self.occupied < self.capacity:
            self.occupied += 1

    def register_exit(self):
        if self.occupied > 0:
            self.occupied -= 1

    @property
    def free_spaces(self) -> int:
        return self.capacity - self.occupied

```
### 7.2 UML Diagrams
- **Use Case Diagram:** Shows how the different components work together.
![Use Case Diagram](Graphics/Use_case_diagramm.svg)

**Datenflussdiagram:** 

![Datenflussdiagramm](Graphics\Datenflussdriagramm.svg)
- **Sequence Diagram:** Visualizes the event loop between sensor/camera, counter, and UI.
---      

### Results of Sprint 1 
*   **Creation of the UI:** a simple UI Built, and connected to the counter,that can be openned on PC and Phone.
*   **Working car Recognition System:** The recognition System has been coded and works.
*   **Counter:** the counter works, it can either add or delete a Parking Space.
*   **Interconnection:** every part of the Programme is connected together. 


---

## 8. Sprint 2 Expansion (Adaptation, Log, UI Design & Testing)
In this sprint, the recognition system was adapted to our program (own thread, webcam), the UI got an exit button, every change of the parking lot is written to a log file and the code is covered by unit tests. The UI design, the stats display, the error rate and the last parts of the documentation are still open (marked with *open*).

### 8.1 User Stories & Task Lists (Estimation in Hours)

**User Story US8:** *"As a coder, I want to have a clean documentation for the project to be legible and simple to modify."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.1 | Document each function of the code directly inside of it. | TBD |
| Task 2.2 | Write in the GitHub the important lines of code and explain how they work (see 8.2). | TBD |
| Task 2.3 | Finish the README: from which side the camera must be pointed, how long to wait until the program works at startup, explanation of abstraction, why lists instead of queues, why abstract classes instead of interfaces, why the program is kept simple. *(open)* | TBD |

**User Story US9:** *"As a User, I want to be able to trust the recognition program, so that the counter can be trusted."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.4 | Write unit tests for the counter, the sensors, the UIs and the main program. | TBD |
| Task 2.5 | Test the counter in combination with the recognition system (real video or camera). *(open)* | TBD |
| Task 2.6 | Set a percentage of errors. *(open)* | TBD |
| Task 2.7 | Analyse the errors and see how we could reduce them. *(open)* | TBD |

**User Story US10:** *"As a User, I want to have additional data on the parking situation in the parking lot (stats)."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.8 | Add a clock to the car counting system: every change gets a time stamp in a log file (time, event, free and occupied lots). | TBD |
| Task 2.9 | Implement a system to show the stats of how many cars are usually on the parking lot at a given time/date. *(open)* | TBD |
| Task 2.10 | Integrate it with the UI. *(open)* | TBD |

**User Story US11:** *"As a User, I want to have a good looking and simple interface, to save some time."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.11 | Find or build a graphic template for the UI to look good and be easy to understand. *(open)* | TBD |
| Task 2.12 | Write the CSS code (at the moment there is only a short style block to center the page). *(open)* | TBD |

**User Story US12:** *"As a coder, I want to build an easy to modify UI, so that I can adapt it to every device and every use."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.13 | Find a way to build a UI that can work on both phone and PC: a web page served by a small web server in the local network. | TBD |
| Task 2.14 | Keep the page (`index.html`) separate from the Python code, so the design can be changed without touching the program. | TBD |
| Task 2.15 | Add an exit button that ends the program and closes the page. | TBD |
| Task 2.16 | Check the page on different devices and adapt it if necessary. *(open)* | TBD |

**User Story US13:** *"As a coder, I want to adapt the recognition system for it to work with our program."*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| Task 2.17 | Think about how the recognition system can be used to count and how to set an output for it. | TBD |
| Task 2.18 | Build the output to the counter: the sensor puts IN/OUT events into the shared list that the main program reads. | TBD |
| Task 2.19 | Run the detection in its own thread, so the program does not freeze. | TBD |
| Task 2.20 | Connect the sensor to a webcam (video input 0) in addition to a video file. | TBD |
| Task 2.21 | Add `requirements.txt` for the camera and detection libraries. | TBD |

---

### 8.2 Key Code Snippets
```python
# counter.py - the counter only knows numbers, nothing about sensors or UI
class PCounter:
    def apply(self, direction: Direction):
        self.occupied = max(0, self.occupied + direction.value)   # IN = +1, OUT = -1, never below 0

    @property
    def free(self) -> int:
        return max(0, self.capacity - self.occupied)              # never below 0, even if the lot is over full
```

```python
# vehicle_sensor.py - decides if a car crossed the counting line and in which direction
@staticmethod
def _crossing_direction(previous, current, line_x=750, line_top=200, line_bottom=700):
    if current[0] == previous[0]:
        return None                                  # no sideways movement, nothing to count
    if previous[0] < line_x <= current[0]:
        direction = Direction.OUT                    # left -> right = car leaves
    elif previous[0] > line_x >= current[0]:
        direction = Direction.IN                     # right -> left = car enters
    else:
        return None                                  # the car did not cross the line

    # y position where the car path meets the line
    crossing_y = previous[1] + (
        (current[1] - previous[1]) * (line_x - previous[0])
        / (current[0] - previous[0])
    )
    # only count it if the crossing is on the real line segment
    return direction if line_top <= crossing_y <= line_bottom else None
```

```python
# logui.py - second, independent UI: writes one line to a text file for every change
def show(self, occupied, free):
    if self._last is None:
        self._log("Start", occupied, free)           # first call = start of the program
    elif occupied > self._last[0]:
        cars = occupied - self._last[0]
        self._log("Car in" if cars == 1 else f"{cars} cars in", occupied, free)
    elif occupied < self._last[0]:
        cars = self._last[0] - occupied
        self._log("Car out" if cars == 1 else f"{cars} cars out", occupied, free)
    self._last = (occupied, free)                    # remember the numbers to see the next change
```

### Results of Sprint 2
*   **Recognition system adapted:** The vehicle sensor runs the detection in its own thread, sends the IN/OUT events to the counter and works with a video file or a webcam.
*   **UI:** The UI has an exit button that ends the program and closes the page.
*   **Log:** Every change of the parking lot is written with the time to a log file (`parkingcounter_log.txt`).
*   **Unit tests:** The counter, the sensors, the UIs and the main program are covered by unit tests (`test/` folder, the target of 70% coverage is reached).
*   **Still open:** UI design (CSS), stats display in the UI, error rate of the recognition and the last parts of the documentation.
