"""
user.py - Module for Managing User Data

This module defines the User class, which handles operations related to users,
including adding, updating, removing, and finding users in a CSV database.
"""

from my_csv import MyCSV

class User:
    """
    User class to manage user information.

    Attributes:
        my_csv (MyCSV): Database for users stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = ['ID', 'Full Name', 'Address', 'Mobile Number', 'Email', 'Password']

    def __init__(self, user_db):
        """
        Initialize the User class with the path to the user database (CSV file).
        :param user_db: Path to the CSV file containing user data.
        """
        if isinstance(user_db, MyCSV):
            self.my_csv = user_db
        else:
            self.my_csv = MyCSV(user_db, User.DEFAULT_FIELDNAMES)

    def add_user(self, user_data):
        """
        Add a new user to the system (CSV file).
        :param user_data: Dictionary containing user data 
        (ID, Full Name, Address, Mobile Number, Email).
        """
        self.my_csv.add_data(user_data)

    def update_user(self, user_id, update_data):
        """
        Update a user's information by their ID.
        :param user_id: Unique identifier for the user.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.my_csv.update_data('ID', user_id, update_data)
        if not updated:
            raise ValueError(f"User with ID {user_id} not found.")

    def remove_user(self, user_id):
        """
        Remove a user from the system by their ID.
        :param user_id: Unique identifier for the user.
        """
        removed = self.my_csv.remove_data('ID', user_id)
        if not removed:
            raise ValueError(f"User with ID {user_id} not found.")

    def find_user_by_id(self, user_id):
        """
        Find a user by their ID.
        :param user_id: Unique identifier for the user.
        :return: Dictionary representing the user or None if not found.
        """
        users = self.my_csv.load_data()
        for user in users:
            if user['ID'] == user_id:
                return user
        return None

    def find_user_by_name(self, full_name):
        """
        Find a user by their full name.
        :param full_name: Full name of the user to search for.
        :return: Dictionary representing the user or None if not found.
        """
        # Load database
        users = self.my_csv.load_data()
        # Search for the user with the matching full name
        for user in users:
            if user['Full Name'] == full_name:
                return user
        return None
