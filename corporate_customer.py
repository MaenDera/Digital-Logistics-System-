"""
corporate_customer.py - Module for Managing Corporate Customers

This module defines the CorporateCustomer class, which handles operations
related to corporate customers, including adding, updating, removing, and
finding corporate customers in a CSV database.
"""
from my_csv import MyCSV
from user import User

class CorporateCustomer:
    """
    CorporateCustomer class to manage corporate customer information.

    Attributes:
        corporate_customer_db (MyCSV): Database for corporate customers.
        user_db (MyCSV): Database for users related to corporate customers.
    """

    DEFAULT_FIELDNAMES = ['ID', 'Company Name',
                          'Company Address',
                          'Reference Person',
                          'Reference Person Contact',
                          'Invoice Email', 'Related Users']

    def __init__(self, corporate_customer_db, user_db):
        """
        Initialize the CorporateCustomer class with the path to 
        the customer and user databases (CSV files).
        :param corporate_customer_db: Path to the CSV file 
        containing corporate customer data.
        :param user_db: Path to the CSV file containing user data.
        """
        if isinstance(corporate_customer_db, MyCSV):
            self.corporate_customer_db = corporate_customer_db
            self.user_db = user_db
        else:
            self.corporate_customer_db = MyCSV(corporate_customer_db,
                                               CorporateCustomer.DEFAULT_FIELDNAMES)
            self.user_db = MyCSV(user_db, User.DEFAULT_FIELDNAMES)

    def add_customer(self, customer_data):
        """
        Add a new corporate customer to the system (CSV file).
        :param customer_data: Dictionary containing corporate customer data.
        """
        self.corporate_customer_db.add_data(customer_data)

    def update_customer(self, customer_id, update_data):
        """
        Update a corporate customer's information by their ID.
        :param customer_id: Unique identifier for the corporate customer.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.corporate_customer_db.update_data('ID', customer_id, update_data)
        if not updated:
            raise ValueError(f"Corporate customer with ID {customer_id} not found.")

    def remove_customer(self, customer_id):
        """
        Remove a corporate customer from the system by their ID.
        :param customer_id: Unique identifier for the corporate customer.
        """
        removed = self.corporate_customer_db.remove_data('ID', customer_id)
        if not removed:
            raise ValueError(f"Corporate customer with ID {customer_id} not found.")

    def find_customer_by_id(self, customer_id):
        """
        Find a corporate customer by their ID.
        :param customer_id: Unique identifier for the corporate customer.
        :return: Dictionary containing the corporate customer data if found, else None.
        """
        # Load all corporate customers from the CSV
        customers = self.corporate_customer_db.load_data()
        # Search for the customer with the matching ID
        for customer in customers:
            if customer['ID'] == customer_id:
                return customer
        return None
