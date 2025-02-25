"""
payment.py - Module for Managing Payment Data

This module defines the Payment class, which handles operations related to
payments, including adding, updating, and finding payments in a CSV database.
"""

from my_csv import MyCSV

class Payment:
    """
    Payment class to manage payment information.

    Attributes:
        payment_db (MyCSV): Database for payments stored in a CSV file.
    """

    DEFAULT_FIELDNAMES = ['Payment Method',
                          'Transaction ID',
                          'Currency', 'Amount',
                          'Payment Status',
                          'Card Information']

    def __init__(self, payment_db):
        """
        Initialize the Payment class with the path to the payment database (CSV file).
        :param payment_db: Path to the CSV file containing payment data.
        """
        if isinstance(payment_db, MyCSV):
            self.payment_db = payment_db
        else:
            self.payment_db = MyCSV(payment_db, Payment.DEFAULT_FIELDNAMES)

    def add_payment(self, payment_data):
        """
        Add a new payment record to the system (CSV file).
        :param payment_data: Dictionary containing payment data.
        """
        self.payment_db.add_data(payment_data)

    def update_payment(self, transaction_id, update_data):
        """
        Update a payment's information by its Transaction ID.
        :param transaction_id: Unique identifier for the payment.
        :param update_data: Dictionary containing updated data.
        """
        updated = self.payment_db.update_data('Transaction ID', transaction_id, update_data)
        if not updated:
            raise ValueError(f"Payment with Transaction ID {transaction_id} not found.")

    def find_payment_by_id(self, transaction_id):
        """
        Find a payment record by its Transaction ID.
        :param transaction_id: Unique identifier for the payment.
        :return: Dictionary representing the payment or None if not found.
        """
        payments = self.payment_db.load_data()
        for payment in payments:
            if payment['Transaction ID'] == transaction_id:
                return payment
        return None
