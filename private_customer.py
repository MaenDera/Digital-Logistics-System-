"""
private_customer.py - Module for Managing Private Customer Data

This module defines the PrivateCustomer class, which handles operations
related to private customers, including adding, updating, removing, and
finding private customers in a CSV database.
"""

from my_csv import MyCSV

class PrivateCustomer:
    """
    PrivateCustomer class to manage private customer information.

    Attributes:
        private_customer_db (MyCSV): Database for private customers stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = ['ID', 'Full Name', 'Address', 'Mobile Number', 'Invoice Email']

    def __init__(self, private_customer_db):
        """
        Initialize the PrivateCustomer class with the path to the customer database (CSV file).
        :param private_customer_db: Path to the CSV file containing private customer data.
        """
        if isinstance(private_customer_db, MyCSV):
            self.corporate_customer_db = private_customer_db
        else:
            self.corporate_customer_db = MyCSV(private_customer_db,
                                               PrivateCustomer.DEFAULT_FIELDNAMES)

    def add_customer(self, customer_data):
        """
        Add a new private customer to the system (CSV file).
        :param customer_data: Dictionary containing private customer data.
        """
        # Add the private customer to the CSV file
        self.corporate_customer_db.add_data(customer_data)

    def update_customer(self, customer_id, update_data):
        """
        Update a private customer's information by their ID.
        :param customer_id: Unique identifier for the private customer.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.corporate_customer_db.update_data('ID', customer_id, update_data)
        if not updated:
            raise ValueError(f"Private customer with ID {customer_id} not found.")

    def remove_customer(self, customer_id):
        """
        Remove a private customer from the system by their ID.
        :param customer_id: Unique identifier for the private customer.
        """
        removed = self.corporate_customer_db.remove_data('ID', customer_id)
        if not removed:
            raise ValueError(f"Private customer with ID {customer_id} not found.")

    def find_customer_by_id(self, customer_id):
        """
        Find a private customer by their ID.
        :param customer_id: Unique identifier for the private customer.
        :return: Dictionary containing customer data if found, otherwise None.
        """
        customers = self.corporate_customer_db.load_data()
        for customer in customers:
            if customer['ID'] == customer_id:
                return customer
        return None
