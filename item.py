"""
item.py - Module for Managing Item Data

This module defines the Item class, which handles operations related to items,
including adding, removing, and finding items in a CSV database.
"""

from my_csv import MyCSV

class Item:
    """
    Item class to manage item information.

    Attributes:
        item_db (MyCSV): Database for items stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = ['ID', 'Price per kg', 'Weight', 'Type']

    def __init__(self, item_db):
        """
        Initialize the Item class with the path to the item database (CSV file).
        :param item_db: Path to the CSV file containing item data.
        """
        if isinstance(item_db, MyCSV):
            self.item_db = item_db
        else:
            self.item_db = MyCSV(item_db, Item.DEFAULT_FIELDNAMES)

    def add_item(self, item_data):
        """
        Add a new item to the system (CSV file).
        :param item_data: Dictionary containing item data.
        """
        self.item_db.add_data(item_data)

    def remove_item(self, item_id):
        """
        Remove an item from the system by its ID.
        :param item_id: Unique identifier for the item.
        """
        removed = self.item_db.remove_data('ID', item_id)
        if not removed:
            raise ValueError(f"Item with ID {item_id} not found.")

    def find_item_by_id(self, item_id):
        """
        Find an item by its ID.
        :param item_id: Unique identifier for the item.
        :return: Dictionary representing the item or None if not found.
        """
        items = self.item_db.load_data()
        for item in items:
            if item['ID'] == item_id:
                return item
        return None
