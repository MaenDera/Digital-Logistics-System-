"""
validation.py - Module for Input Validation

This module provides a Validation class that includes static methods for
validating various types of user inputs, including names, mobile numbers,
email addresses, and payment details.
"""

import re
from datetime import datetime, timedelta

class Validation:
    """
    Validation class for checking all user input.

    This class provides static methods to validate different types of input,
    such as names, mobile numbers, emails, passwords, and payment details.
    Each method prompts the user for input and ensures that the input meets
    the specified criteria.
    """
    @staticmethod
    def check_input_name(attribute_name:str):
        """
        Validate that the input name consists of a first and last name.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated name formatted with title case.
        """
        while True:
            attribute = input(f'Enter {attribute_name}: ').strip()

            # Check if the input contains only letters and a space between names
            if all(part.isalpha() for part in attribute.split()) and len(attribute.split()) == 2:
                return attribute.title()
            print(f"Error: {attribute_name} should contain only first and last name "
                  "with alphabetical characters (e.g., Mike Smith).")

    @staticmethod
    def check_input_mobile(attribute_name:str):
        """
        Validate mobile number format.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated mobile number.
        """
        _mobile = r'^07\d{8}$'
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if re.match(_mobile, attribute):
                return attribute
            print(f"Error: {attribute_name} should start with '07' and followed by"
                  "8 digits (e.g., 0712345678).")

    @staticmethod
    def check_input_alpha_numeric(attribute_name:str):
        """
        Validate that the input is alphanumeric.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated alphanumeric string.
        """
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if attribute.isalnum():
                return attribute
            print(f"Error: {attribute_name} should have only digits or alphabetical characters.")

    @staticmethod
    def check_input_zip_code(attribute_name: str) -> str:
        """
        Validate the zip code format.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated zip code.
        """
        _zip_code_pattern = r'^\d{5}$'
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if re.match(_zip_code_pattern, attribute):
                return attribute
            print(f"Error: {attribute_name} must be exactly 5 digits.")

    @staticmethod
    def check_input_email(attribute_name:str):
        """
        Validate email format.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated email address.
        """
        _email = r'^[\w\.-]+@[\w\.-]+\.\w{2,3}$'
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if re.match(_email, attribute):
                return attribute
            print(f"Error: {attribute_name} should be in a valid"
                  "email format (e.g., example@example.com).")

    @staticmethod
    def check_input_password(attribute_name:str):
        """
        Validate the password format.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated password.
        """
        _password = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if re.match(_password, attribute):
                return attribute
            print(f"Error: {attribute_name} should be at least 8 characters long, "
                  "contain at least one letter, one digit, and one special character (@$!%*#?&).")

    @staticmethod
    def check_company_city_country_name(attribute_name:str):
        """
        Validate that the input consists of alphabetical characters only.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated city or country name.
        """
        while True:
            attribute = input(f"Enter {attribute_name}: ")
            if attribute.isalpha():
                return attribute.title()
            print(f"Error: {attribute_name} should have only alphabetical characters.")

    @staticmethod
    def check_item_type(attribute_name:str):
        """
        Validate the type of the item.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated item type.
        """
        _type = ['fragile', 'solid']
        while True:
            attribute = input(f'Enter {attribute_name} (fragile/solid):').lower().strip()
            if attribute.isalpha() and attribute in _type:
                return attribute
            print(f"Error: {attribute_name} should be either 'fragile' or 'solid'"
                  "and contain only alphabetical characters.")

    @staticmethod
    def check_payment_method(attribute_name: str):
        """
        Validate the payment method.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated payment method.
        """
        _payment_methods = ["credit", "debit"]
        while True:
            attribute = input(f'Enter {attribute_name} (Credit/Debit) Card:').lower().strip()
            if attribute in _payment_methods:
                return attribute
            print(f"Error: {attribute_name} should be one of the following:"
                  "Credit Card, or Debit Card.")

    @staticmethod
    def check_currency(attribute_name:str):
        """
        Validate the currency input.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated currency.
        """
        _currency = ["€", "SEK"]
        while True:
            attribute = input(f'Enter {attribute_name} (€/SEK):').upper().strip()
            if attribute in _currency:
                return attribute
            print(f"Error: {attribute_name} should be either '€' or 'SEK'.")

    @staticmethod
    def check_payment_status(attribute_name:str):
        """
        Validate the payment status.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated payment status.
        """
        _payment_status = ["paid", "unpaid"]
        while True:
            attribute = input(f'Enter {attribute_name} (paid/unpaid):').lower().strip()
            if attribute in _payment_status:
                return attribute
            print(f"Error: {attribute_name} should be either 'paid' or 'unpaid'.")

    @staticmethod
    def check_card_info(attribute_name: str):
        """
        Validate card information.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Dictionary containing validated card information.
        """
        print(f'{attribute_name}\n')
        while True:
            card_number = input('Enter Card Number (16 digits): ').strip()
            if card_number.isdigit() and len(card_number) == 16:
                cardholder_name = Validation.check_input_name("Cardholder Name")
                # Get expiration date and validate it
                expiration_date = input('Enter Expiration Date (MM/YY): ').strip()
                if Validation.validate_expiration_date(expiration_date):
                    # Get CVV and validate it
                    cvv = input('Enter CVV (3 digits): ').strip()
                    if cvv.isdigit() and len(cvv) == 3:
                        return {
                            "card_number": card_number,
                            "cardholder_name": cardholder_name,
                            "expiration_date": expiration_date,
                            "cvv": cvv
                        }
                    print("Error: CVV must be exactly 3 digits and numeric.")
                print("Error: Expiration date must be in the format MM/YY"
                      "and valid within the next 5 years.")
            print("Error: Card number must be exactly 16 digits and numeric.")

    @staticmethod
    def validate_expiration_date(expiration_date: str) -> bool:
        """
        Validate the expiration date format and its validity.
        
        :param expiration_date: Expiration date string in MM/YY format.
        :return: True if valid, False otherwise.
        """
        # Check if the expiration date matches the MM/YY format
        if len(expiration_date) == 5 and expiration_date[2] == '/':
            month_part = expiration_date[:2]
            year_part = expiration_date[3:]
            # Get the current year and calculate the valid range
            current_year = datetime.now().year % 100
            valid_year_range = [(current_year + i) % 100 for i in range(6)]
            # Validate the month and year
            return (month_part.isdigit() and
                    year_part.isdigit() and
                    1 <= int(month_part) <= 12 and
                    int(year_part) in valid_year_range)
        return False

    @staticmethod
    def check_priority(attribute_name:str):
        """
        Validate the priority input.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated priority.
        """
        _priority = ["low", "medium", "high"]
        while True:
            attribute = input(f'Enter {attribute_name} (Low/Medium/High):').strip().lower()
            if attribute in _priority:
                return attribute
            print(f"Error: {attribute_name} should be either 'Low', 'Medium', or 'High'.")

    @staticmethod
    def check_positive_integer(attribute_name: str) -> int:
        """
        Validate that the input is a positive integer.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated positive integer.
        """
        while True:
            try:
                attribute = int(input(f'{attribute_name}: '))
                if attribute <= 0:
                    print("Error: The number must be a positive integer. Please try again.")
                else:
                    return int(attribute)
            except ValueError:
                print("Error: Please enter a valid integer.")

    @staticmethod
    def check_positive_float(attribute_name:str) -> float:
        """
        Validates that the input is a positive floating-point number.
        """
        while True:
            try:
                attribute = float(input(f'Enter {attribute_name}: '))
                if attribute < 0:
                    print("Error: The number must be a positive float. Please try again.")
                else:
                    return attribute
            except ValueError:
                print("Error: Please enter a valid floating-point number.")

    @staticmethod
    def validate_id(attribute_name:str):
        """
        Validate the ID format.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated ID.
        """
        while True:
            attribute = input(f"Enter {attribute_name}: ").upper()

            # Allow 'x' to break the loop
            if attribute.lower() == 'x':
                return 'x'
            # Check if the first character is alphabetic and the rest are digits
            if len(attribute) == 5 and attribute[0].isalpha() and attribute[1:].isdigit():
                return attribute
            print(f"Error: {attribute_name} should start with a letter"
                  "followed by 4 digits (e.g., U1234).")

    @staticmethod
    def get_delivery_date():
        """
        Get a valid delivery date from user input.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated delivery date in YYYY-MM-DD format.
        """
        while True:
            try:
                date_input = input("Enter the delivery date (YYYY-MM-DD): ")
                delivery_date = datetime.strptime(date_input, '%Y-%m-%d')
                # Check if the delivery date is at least 2 days in the future
                if delivery_date >= datetime.now() + timedelta(days=2):
                    return delivery_date.strftime('%Y-%m-%d')
                print("Error: The delivery date must be at least 2 days in the future.")
            except ValueError:
                print("Error: Please enter a valid date in the format YYYY-MM-DD.")

    @staticmethod
    def check_order_status(attribute_name:str):
        """
        Validate the order status.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated order status.
        """
        _order_status = ["delivered", "processing", "canceled"]
        while True:
            attribute = input(f'Enter {attribute_name} (Delivered/Processing/Canceled):').strip().lower()
            if attribute in _order_status:
                return attribute
            print(f"Error: {attribute_name} should be either"
                  "'Delivered', 'Processing', or 'Canceled'.")

    @staticmethod
    def validate_transaction_id(attribute_name):
        """
        Validate the ID format for transactions.
        
        :param attribute_name: The name of the attribute being checked.
        :return: Validated transaction ID.
        """
        while True:
            attribute = input(f"Enter {attribute_name}: ").upper()
            # Allow 'x' to break the loop
            if attribute.lower() == 'x':
                return 'x'
            # Check if the first two characters are alphabetic
            # and the next four characters are digits
            if len(attribute) == 6 and attribute[:2].isalpha() and attribute[2:].isdigit():
                return attribute
            print(f"Error: {attribute_name} should start with two letters followed by 4 digits (e.g., Tr1234).")
