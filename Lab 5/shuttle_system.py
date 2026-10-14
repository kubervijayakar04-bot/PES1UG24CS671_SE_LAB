"""Track campus shuttle routes, passenger loads, and fleet data."""

import json
import secrets
from datetime import datetime
from pathlib import Path

MIN_CAPACITY = 10
DRIVERS = ("Prakash", "Leela", "Imran", "Tom")

routes = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a valid passenger count for a known route."""
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    if isinstance(passenger_count, bool) or not isinstance(
        passenger_count, int
    ):
        raise TypeError("Passenger count must be an integer.")
    if passenger_count < 0:
        raise ValueError("Passenger count cannot be negative.")

    if logs is None:
        logs = []

    routes[route_id]["trips"].append(passenger_count)
    timestamp = datetime.now().isoformat(timespec="seconds")
    logs.append(f"{timestamp}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Remove a route, raising a clear error if it does not exist."""
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    del routes[route_id]


def average_load(route_id):
    """Return the average passengers per trip for a known route."""
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")

    trips = routes[route_id]["trips"]
    if not trips:
        return 0.0
    return sum(trips) / len(trips)


def underused_routes():
    """Return routes whose average passenger load is below capacity."""
    return [
        route_id
        for route_id in routes
        if average_load(route_id) < MIN_CAPACITY
    ]


def assign_driver(route_id):
    """Assign a driver to a known route."""
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    return secrets.choice(DRIVERS)


def sync_fleet_data(filename="fleet.json"):
    """Write the current route data to a JSON file."""
    fleet_path = Path(filename)
    with fleet_path.open("w", encoding="utf-8") as fleet_file:
        json.dump(routes, fleet_file, indent=2, ensure_ascii=False)


def main():
    """Run a small demonstration of the campus shuttle tracker."""
    trip_logs = []
    add_trip_log("R1", 32, trip_logs)
    add_trip_log("R1", 28, trip_logs)
    add_trip_log("R2", 4, trip_logs)
    add_trip_log("R2", 6, trip_logs)
    add_trip_log("R3", 18, trip_logs)

    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))

    choice = input("Route to look up (Enter for R2): ") or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print(f"Unknown route: {choice}")

    print("R3 average:", average_load("R3"))
    remove_route("R3")
    sync_fleet_data()


if __name__ == "__main__":
    main()
