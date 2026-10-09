
# Project Documentation: ParkingCounter

## 1. Introduction, Objectives, Constraints
### 1.1 Introduction
ParkingCounter is a program that uses a webcam to monitor the entrance of a parking area. It detects vehicles entering and leaving the parking area, keeps track of occupied and available spaces and displays the current number of available parking lots through an interface.

### 1.2 Objectives
The main goal is to create a working prototype (MVP) that:
*   Monitors the entrance of a parking area using a **webcam**.
*   Detects vehicles entering and leaving the parking area in real time.
*   Counts the number of occupied and free parking spaces across the entire parking Area.
*   Displays the current number of available parking spaces via a **User Interface**.
*   Provides data for later evaluation.

### 1.3 MVP (Minimum Viable Product)
*   **Control unit:** A computer that can run Python
*   **Sensors:** A Webcam
*   **Output:** User Interface
*   **Software:** Python script using a image detection library.

### 1.4 Constraints
*   Programming language: **Python**.
*   Version control: **GitHub**.
*   Development model: **Scrum** (3 sprints).

---

## 2. Build Instructions
To set up the project locally, follow these steps:
1.  **Clone the repository:** `git clone https://github.com/username/parkfeld-detektor.git`
2.  **Create a virtual environment:** `python -m venv venv`
3.  **Install dependencies:** `pip install -r requirements.txt`
4.  **Start the application:** ....

---

## 3. Brief User Guide
1.  Start the Programm
2.  Open the User Interface
3.  Point your webcam at the entrance to the parking lot

---

## 4. Release Plan with Expansion Stages
*  **Release 0.1 (Sprint 0):**
    - Hardware setup,
    - Project structure on GitHub,
    - HelloWorld
*   **Release 0.2 (Sprint 1 - MVP):**
    - ...
*   **Release 1.0 (Sprint 2):**
    - ...
---

## 5. User Stories
Requirements are described in the form of user stories with acceptance criteria:

| ID | User Story | Acceptance Criterion | Effort (SP) | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **US0** | As a product owner, I want to set up the project initially (GitHub repository, Jira project, release plan, Hello World), so the team can start development efficiently. | Repository and Jira project are created, all team members have access, the repository is cloned locally, and a “Hello World” runs on every computer. | 5 | High |
| **US1** | As a driver, I want to see from the user Interface how many free parking lots are available. | User Interface works and shows the number of available spaces. | 5 | High |
| **US2** | As an operator, I want reliable detection. | Correct status change in 10/10 test cases. | 8 | Medium |

## 6. Sprint 0 Documentation (Preparation & Setup)
Sprint 0 focused on creating the organizational and technical foundation for developing the parking space occupancy detector.

### Task List for Sprint 0:
*   **Requirements analysis:** Creation and definition of the initial **user stories** and setting the **MVP scope**.
*   **Estimation & prioritization:** Assigning **story points** to user stories and prioritizing them in the product backlog.
*   **Infrastructure setup:**
    *   Creation of the **GitHub repository** and invitation of all team members as collaborators.
    *   Setup of a **Jira project** for backlog and sprint management.
*   **Local development setup:**
    *   Successful cloning of the repository by all group members.
    *   Ensuring a **“Hello World” script** compiles and runs on each local computer.

    | Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| T0.1 | Creation of requirements (user stories) including estimation and prioritization. | 4.0 |
| T0.2 | Creation of a **JIRA project** for backlog management and sprint control. | 2.0 |
| T0.3 | Creation of the **GitHub repository** and adding collaborators. | 1.5 |
| T0.4 | Local cloning of the repository on each computer and running a **“HelloWorld”** to test the functionality | 2.0 |
| T0.5 | Creation of the first **release plan** (timeline and expansion stages). | 1.5 |
| T0.6 | **Documentation** creation of the first chapters in Readme.md | 2.5 |

### Results of Sprint 0
*   **Release plan:** Creation of an initial timeline and definition of the expansion stages.
*   **Documentation foundation:** The Documentation is created on Github as readme.md and initial structure is added to fill out later.
*   **Technical framework:** Decision which image recognition library to use
*   **Documentation:** Fill the first chapters in Readme.md.

### Enrichment of the User Stories for the Implementation

### UML Package, Class and Sequence Diagrams

### Documentation of Important Code Snippets

### Derivation of Test Cases from the Acceptance Criteria of the User Stories

---

## 7. Sprint 1 Documentation (MVP Implementation)
...
<!---
In this sprint, the **Minimum Viable Product** was realized: the basic functionality for distance measurement and visual signaling for two parking spaces.

### 7.1 Task List (Estimation in Hours)

**User Story US1: Visual Parking Space Detection**
*“As a driver, I want to see from an LED whether a space is free in order to reduce time spent searching for a parking spot.”*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| T1.1 | **Hardware wiring** of the ESP32 with ultrasonic sensors and LEDs. | 3.5 |
| T1.2 | Implementation of the `DistanceSensor` class in Python. | 4.0 |
| T1.3 | Programming the control logic for status changes (occupied/free). | 3.0 |
| T1.4 | Creation of **unit tests** for the logic class (target: 50% coverage). | 3.0 |
| T1.5 | **Documentation** of classes as class diagrams | 1.5 |
| T1.6 | **Documentation** of workflows as sequence diagrams | 1.5 |


### 7.2 UML Diagrams
*   **Package diagram:** Structuring the modules (sensors, logic, display).
*   **Class diagram:** Shows the `ParkfeldController` class, which manages two instances of `UltraschallSensor`.
*   **Sequence diagram:** Visualizes the loop: sensor measures distance → controller checks threshold → LED is switched.

Example class diagram (excerpt):
```mermaid
classDiagram
    class ParkfeldController {
        +update_status(distance)
    }
    class UltraschallSensor {
        +distance()
    }
    class LED {
        +on()
        +off()
    }
    ParkfeldController ->UltraschallSensor : uses
    ParkfeldController -> LED : controls
```

### 7.3 Key Code Snippets
```python
# Logic for determining the status (excerpt from ParkfeldController)
def update_status(self, distance):
    if distance < self.threshold:
        self.led_red.on()
        self.led_green.off()
    else:
        self.led_red.off()
        self.led_green.on()
```
*This code ensures that the requirements for visual feedback are met.*

### 7.4 Derivation of Test Cases
| ID | Acceptance Criterion (from US) | Test Case | Result |
| :--- | :--- | :--- | :--- |
| **C1.1** | Red LED when distance < 100 cm | Place an object 50 cm away | Red LED lights up |
| **C1.2** | Green LED when distance > 100 cm | Remove object | Green LED lights up |

---

## 8. Sprint 2 Documentation (Expansion Implementation)
The focus of Sprint 2 is **optimization** and the implementation of a **logging function** to monitor parking usage.

### 8.1 Task List (Estimation in Hours)

**User Story US2: Data Logging and System Stability**
*“As an operator, I want reliable detection and logging of occupancy duration for usage analysis.”*

| Task-ID | Description | Effort (h) |
| :--- | :--- | :--- |
| T2.1 | Implementation of a **moving average filter** to suppress sensor noise. | 3.5 |
| T2.2 | Development of a `Logger` module to store status changes in a CSV file. | 4.0 |
| T2.3 | Conducting manual **black-box tests** including logging. | 2.0 |
| T2.4 | Code refactoring to comply with programming conventions and clean code. | 2.5 |

### 8.2 UML Diagrams
*   **Package diagram:** Extension of the `Storage` package for logging.
*   **Sequence diagram:** Extended flow including the write operation to the ESP32 flash memory upon status change.

### 8.3 Key Code Snippets
```python
# Moving average filter to suppress noise
def get_filtered_distance(self):
    measurements = [self.sensor.distance() for _ in range(5)]
    return sum(measurements) / len(measurements)
```
*This filter improves the stability of the system under unstable sensor values.*

### 8.4 Derivation of Test Cases & Black-Box Testing
*   **Unit test (logging):** Verifies that the file `log.csv` was written correctly after a status change.
*   **Black-box test (manual):**
    | Action | Expected Result | Status |
    | :--- | :--- | :--- |
    | Quick movement in front of the sensor | No LED flicker thanks to the filter | OK |
    | Interrupt power supply | Last status remains in the log | OK |

---

## 9. Optional: Sprint 3 Documentation (Completion & Web Interface)
*(If applicable: Further features such as a simple web dashboard on the ESP32 can be documented here.)*

### Conclusion
The system fulfills all requirements of the specification. The agile approach helped identify technical hurdles in sensor calibration early on.
 zuverlässige Erkennung und ein Logging der Belegungsdauer zur Nutzungsanalyse“*.
| Task-ID | Beschreibung | Aufwand (h) |
| :--- | :--- | :--- |
| T2.1 | Implementierung eines **Mittelwert-Filters** zur Rauschunterdrückung der Sensordaten. | 3.5 |
| T2.2 | Entwicklung eines `Logger`-Moduls zur Speicherung von Statuswechseln in einer CSV-Datei. | 4.0 |
| T2.3 | Durchführung von manuellen **Blackbox-Tests** inkl. Protokollierung. | 2.0 |
| T2.4 | Code-Refactoring zur Einhaltung von Programmierkonventionen und Clean Code. | 2.5 |

### 8.2 UML-Diagramme
*   **Package-Diagramm:** Ergänzung des Pakets `Storage` für das Logging.
*   **Sequenzdiagramm:** Erweiterter Ablauf inklusive des Schreibvorgangs auf den Flash-Speicher des ESP32 bei Statusänderung.

### 8.3 Wichtige Code-Snippets
```python
# Mittelwert-Filter zur Rauschunterdrückung
def get_filtered_distance(self):
    measurements = [self.sensor.distance() for _ in range(5)]
    return sum(measurements) / len(measurements)
```
*Dieser Filter verbessert die Stabilität des Systems bei instabilen Sensorwerten.*

### 8.4 Herleitung der Testfälle & Blackbox-Testing
*   **Unit-Test (Logging):** Überprüft, ob die Datei `log.csv` nach einem Statuswechsel korrekt beschrieben wurde.
*   **Blackbox-Test (Manuell):**
    | Aktion | Erwartetes Resultat | Status |
    | :--- | :--- | :--- |
    | Schnelle Bewegung vor Sensor | Kein LED-Flackern dank Filter | OK |
    | Stromzufuhr unterbrechen | Letzter Status bleibt im Log erhalten | OK |

---

## 9. Optional: Dokumentation Sprint 3 (Abschluss & Web-Interface)
*(Falls zutreffend: Hier können weitere Features wie ein einfaches Web-Dashboard auf dem ESP32 dokumentiert werden.)*

### Fazit der Arbeit
Das System erfüllt alle Anforderungen des Pflichtenhefts. Die agile Vorgehensweise half, technische Hürden bei der Sensorkalibrierung frühzeitig zu erkennen.
-->
