"""
order.py - Module for Managing Order Data

This module defines the Order class, which handles operations related to
orders, including adding, updating, and finding orders in a CSV database.
"""

from my_csv import MyCSV

class Order:
    """
    Order class to manage order information.

    Attributes:
        order_db (MyCSV): Database for orders stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = [
            'Order ID', 'Priority', 'Customer', 'Delivery Location', 'Payment Details', 'Items', 
            'Total Weight', 'Order Status', 'Order Date', 'Delivery Date', 'Vehicle'
        ]

    def __init__(self, order_db):
        """
        Initialize the Order class with the path to the order database (CSV file).
        :param order_db: Path to the CSV file containing order data.
        """
        if isinstance(order_db, MyCSV):
            self.order_db = order_db
        else:
            self.order_db = MyCSV(order_db, Order.DEFAULT_FIELDNAMES)

    def add_order(self, order_data):
        """
        Add a new order to the system (CSV file).
        :param order_data: Dictionary containing order data.
        """
        self.order_db.add_data(order_data)

    def update_order(self, order_id, update_data):
        """
        Update an order's information by its ID.
        :param order_id: Unique identifier for the order.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.order_db.update_data('Order ID', order_id, update_data)
        if not updated:
            raise ValueError(f"Order with ID {order_id} not found.")

    def find_order_by_id(self, order_id):
        """
        Find an order by its ID.
        :param order_id: Unique identifier for the order.
        :return: Dictionary representing the order or None if not found.
        """
        orders = self.order_db.load_data()
        for order in orders:
            if order['Order ID'] == order_id:
                return order
        return None
