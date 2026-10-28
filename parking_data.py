from flask import Flask, jsonify, request, render_template
from ui_interface import IUI

class WebParkingUI(IUI):
    """
    Concrete implementation of the user interface for the Web application.
    Inherits from IUI defined in ui_interface.py.
    """

    def __init__(self, capacity: int = 50, start_occupied: int = 0):
        # Call the constructor of the parent class IUI
        super().__init__(capacity=capacity, start_occupied=start_occupied)
        self.occupied = start_occupied

    def start(self):
        """Start the UI component."""
        print(f"[SERVER STARTED] Initial capacity: {self.capacity}")

    def show(self, occupied: int, free: int):
        """
        Calculates and updates internal values, then prints status to console.
        """
        self.occupied = occupied
        # Free spaces cannot be negative (clamped to 0 using max)
        free_spaces = max(0, self.capacity - self.occupied)
        print(f"[STATUS UPDATE] Capacity: {self.capacity} | Occupied: {self.occupied} | Free: {free_spaces}")

    def set_new_capacity(self, new_capacity: int):
        """
        Updates the parking capacity and recalculates space metrics.
        """
        if new_capacity >= 0:
            self.capacity = new_capacity
            # Trigger recalculation using show method
            self.show(self.occupied, self.get_free_spaces())

    def get_free_spaces(self) -> int:
        """Returns the number of available parking spaces."""
        return max(0, self.capacity - self.occupied)

    def to_dict(self) -> dict:
        """Returns the current state formatted for JSON API response."""
        return {
            "capacity": self.capacity,
            "occupied": self.occupied,
            "free": self.get_free_spaces()
        }


# Initialize Flask application
app = Flask(__name__, template_folder=".")

# Instantiate our custom UI class (Default capacity: 50, start occupied: 0)
ui = WebParkingUI(capacity=50, start_occupied=0)


@app.route("/")
def UI():
    """Serves the main HTML interface."""
    return render_template("UI.html")


@app.route("/data", methods=["GET"])
def get_data():
    """
    API Endpoint: Returns current parking statistics (capacity, occupied, free).
    """
    return jsonify(ui.to_dict())


@app.route("/set_capacity", methods=["POST"])
def set_capacity():
    """
    API Endpoint: Receives a new capacity setting from the manager via HTML.
    Expects JSON body: {"capacity": <number>}
    """
    try:
        data = request.get_json(force=True)
        if data and "capacity" in data:
            new_capacity = int(data["capacity"])
            
            # Update capacity using class method
            ui.set_new_capacity(new_capacity)
            
            return jsonify({"status": "success", "data": ui.to_dict()}), 200
        else:
            return jsonify({"status": "error", "message": "Missing 'capacity' field"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/car_in", methods=["POST"])
def car_in():
    """
    API Endpoint: To be called by camera system when a car enters the parking lot.
    """
    if ui.occupied < ui.capacity:
        ui.occupied += 1
        ui.show(ui.occupied, ui.get_free_spaces())
    return jsonify(ui.to_dict())


@app.route("/car_out", methods=["POST"])
def car_out():
    """
    API Endpoint: To be called by camera system when a car leaves the parking lot.
    """
    if ui.occupied > 0:
        ui.occupied -= 1
        ui.show(ui.occupied, ui.get_free_spaces())
    return jsonify(ui.to_dict())


if __name__ == "__main__":
    ui.start()
    app.run(host="0.0.0.0", port=5000, debug=True)