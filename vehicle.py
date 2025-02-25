"""
vehicle.py - Module for Managing Vehicle Data

This module defines the Vehicle class, which handles operations related to
vehicles, including adding, updating, and removing vehicles in a CSV database.
"""

from my_csv import MyCSV

class Vehicle:
    """
    Vehicle class to manage vehicle information.

    Attributes:
        vehicle_db (MyCSV): Database for vehicles stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = ['Vehicle ID', 'Type',
                          'Max Capacity (Weight)',
                          'Max Capacity (Item Count)',
                          'Remaining Capacity (Weight)',
                          'Remaining Capacity (Item Count)',
                          'Current Position', 'Status']

    def __init__(self, vehicle_db):
        """
        Initialize the Vehicle class with the path to the vehicle database (CSV file).
        :param vehicle_db: Path to the CSV file containing vehicle data.
        """
        if isinstance(vehicle_db, MyCSV):
            self.vehicle_db = vehicle_db
        else:
            self.vehicle_db = MyCSV(vehicle_db, Vehicle.DEFAULT_FIELDNAMES)

    def add_vehicle(self, vehicle_data):
        """
        Add a new vehicle to the system (CSV file).
        :param vehicle_data: Dictionary containing vehicle data.
        """
        self.vehicle_db.add_data(vehicle_data)

    def update_vehicle(self, vehicle_id, update_data):
        """
        Update a vehicle's information by its ID.
        :param vehicle_id: Unique identifier for the vehicle.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.vehicle_db.update_data('Vehicle ID', vehicle_id, update_data)
        if not updated:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found.")

    def remove_vehicle(self, vehicle_id):
        """
        Remove a vehicle from the system by its ID.
        :param vehicle_id: Unique identifier for the vehicle.
        """
        removed = self.vehicle_db.remove_data('Vehicle ID', vehicle_id)
        if not removed:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found.")

    def find_vehicle_by_id(self, vehicle_id):
        """
        Find a vehicle by its ID.

        This method searches the vehicle database for a vehicle with the given
        vehicle ID. If the vehicle is found, it returns the vehicle's data.

        :param vehicle_id: Unique identifier for the vehicle.
        :return: Dictionary containing the vehicle data if found, otherwise None.
        """
        vehicles = self.vehicle_db.load_data()
        for vehicle in vehicles:
            if vehicle['Vehicle ID'] == vehicle_id:
                return vehicle
        return None
