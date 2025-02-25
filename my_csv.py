"""
my_csv.py - Module for Managing CSV File Operations

This module defines the MyCSV class, which provides methods for adding,
removing, updating, and loading data from a CSV file.
"""

import csv
import os

class MyCSV:
    """
    MyCSV class for managing CSV file operations.

    Attributes:
        folder (str): The folder where the CSV files are stored.
        file_path (str): The path to the CSV file.
        fieldnames (list): The headers for the CSV file.
    """

    def __init__(self, file_path, fieldnames):
        """
        Initialize the MyCSV class with a file path and fieldnames.
        :param file_path: Path to the CSV file.
        :param fieldnames: List of field names (column headers).
        """
        self.folder = 'database'
        self.file_path = os.path.join(self.folder, file_path)
        self.fieldnames = fieldnames

        # Ensure the database folder exists
        os.makedirs(self.folder, exist_ok=True)

        # Check if the file exists; if not, create it with headers
        if not os.path.isfile(self.file_path):
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames, delimiter=',')
                writer.writeheader()

    def add_data(self, new_entry):
        """
        Add a row to the CSV file.
        :param row_data: Dictionary containing data to be added.
        """
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(new_entry)

    def load_data(self):
        """
        Read all rows from the CSV file.
        :return: List of dictionaries where each dict represents a row.
        """
        data = list()
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def remove_data(self, search_field, search_value):
        """
        Remove a row from the CSV file where the search_field matches search_value.
        :param search_field: Field to search by (column name).
        :param search_value: Value to match in the search_field.
        :return: True if row was removed, False if not.
        """
        rows = self.load_data()
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            removed = False
            for row in rows:
                if row[search_field] != search_value:
                    writer.writerow(row)
                else:
                    removed = True
        return removed

    def update_data(self, search_field, search_value, update_data):
        """
        Update a row in the CSV file where the search_field matches search_value.
        :param search_field: Field to search by (column name).
        :param search_value: Value to match in the search_field.
        :param update_data: Dictionary of values to update.
        :return: True if row was updated, False if not.
        """
        rows = self.load_data()
        updated = False
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for row in rows:
                if row[search_field] == search_value:
                    row.update(update_data)
                    updated = True
                writer.writerow(row)
        return updated  
