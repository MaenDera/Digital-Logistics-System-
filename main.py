"""
main.py - Logistics System Main Module

This module serves as the core of the logistics system. It handles user management,
vehicle management, shipment orders, payments, and customer interactions. The Main class 
provides the methods to manage these operations,
allowing interaction through a command-line interface.
"""

import random
import csv
from datetime import datetime
from my_csv import MyCSV
from validation import Validation
from user import User
from address import Address
from location import Location
from private_customer import PrivateCustomer
from corporate_customer import CorporateCustomer
from vehicle import Vehicle
from order import Order
from payment import Payment
from item import Item

class Main:
    """
    Main class for managing logistics system operations.

    This class provides the functionality to manage users, vehicles, shipments/orders, 
    payments, corporate and private customers, and item management. It also serves as the 
    entry point of the application, where users can interact with the system through various menus.
    """
    def __init__(self):
        """Initialize each database using the default field names from respective classes"""
        self.user_db = MyCSV('user.csv', User.DEFAULT_FIELDNAMES)
        self.corporate_customer_db = MyCSV('corporate_customer.csv',
                                           CorporateCustomer.DEFAULT_FIELDNAMES)
        self.private_customer_db = MyCSV('private_customer.csv', PrivateCustomer.DEFAULT_FIELDNAMES)
        self.vehicle_db = MyCSV('vehicle.csv', Vehicle.DEFAULT_FIELDNAMES)
        self.payment_db = MyCSV('payment.csv', Payment.DEFAULT_FIELDNAMES)
        self.order_db = MyCSV('order.csv', Order.DEFAULT_FIELDNAMES)
        self.item_db = MyCSV('item.csv', Item.DEFAULT_FIELDNAMES)


    # Generate IDs
    def load_existing_ids(self):
        """Load all existing IDs from the relevant databases."""
        existing_ids = set()

        # Load IDs from user database
        existing_ids.update(self.load_ids_from_csv(self.user_db.file_path, 'ID'))
        # Load IDs from corporate customer database
        existing_ids.update(self.load_ids_from_csv(self.corporate_customer_db.file_path, 'ID'))
        # Load IDs from private customer database
        existing_ids.update(self.load_ids_from_csv(self.private_customer_db.file_path, 'ID'))
        # Load IDs from vehicle database
        existing_ids.update(self.load_ids_from_csv(self.vehicle_db.file_path, 'ID'))
        # Load IDs from payment database
        existing_ids.update(self.load_ids_from_csv(self.payment_db.file_path, 'ID'))
        # Load IDs from order database
        existing_ids.update(self.load_ids_from_csv(self.order_db.file_path, 'ID'))

        return existing_ids

    def load_ids_from_csv(self, filename, id_column):
        """Load IDs from a specified column in a CSV file."""
        ids = set()
        encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']  # Common encodings
        for encoding in encodings:
            try:
                with open(filename, mode='r', newline='', encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    ids = [row[id_column] for row in reader if id_column in row]
                # print(f"Successfully read {filename} with {encoding} encoding.")
                break  # If reading succeeds, break out of the loop
            except UnicodeDecodeError:
                if encoding == encodings[-1]:
                    print(f"Unable to read {filename}. Please check the file encoding.")
            except FileNotFoundError:
                print(f"File not found: {filename}")
                break
        return ids

    def generate_unique_id(self, id_type):
        """Generate a unique ID with the specified id type."""
        existing_ids = self.load_existing_ids()
        while True:
            # Generate a new ID
            unique_id = f"{id_type}{random.randint(1000, 9999)}"
            if unique_id not in existing_ids:
                return unique_id


    # User Management Methods
    def get_address(self):
        """
        Collects address data from user input.
        """
        print('\n----- Address Details -----\n')
        street = Validation.check_input_alpha_numeric('Street')
        building_nr = Validation.check_input_alpha_numeric("Building Number")
        zip_code = Validation.check_input_zip_code("Zip Code")
        city = Validation.check_company_city_country_name('Cty')
        print()
        return Address(street, int(building_nr), int(zip_code), city)

    def add_user_main(self):
        """
        Collect user data and add it to the system.
        """
        # Automatically generate a unique user ID with the id type 'U'
        user_id = self.generate_unique_id('U')
        full_name = Validation.check_input_name("Full Name")
        address = self.get_address()
        mobile_number = Validation.check_input_mobile("Mobile Number")
        email = Validation.check_input_email("Email")
        password = Validation.check_input_password("Password")

        # Pack user data into a dictionary
        user_data = {
            'ID': user_id,
            'Full Name': full_name,
            'Address': address,
            'Mobile Number': mobile_number,
            'Email': email,
            'Password': password
        }
        # Instead of creating a new Main instance, create a User instance using the existing user_db
        user = User(self.user_db)
        user.add_user(user_data)
        print(f"User {full_name} added successfully!\n")

    def remove_user_main(self):
        """
        Remove a user from the system by their ID.
        """
        print("Type 'x' to go back")
        user_id = Validation.validate_id('User ID')
        user = User(self.user_db)

        try:
            user.remove_user(user_id)
            print(f"User with ID {user_id} has been removed successfully.")
        except ValueError as e:
            print(e)

    def update_user_main(self):
        """
        Update a user's information in the system by their ID.
        """
        print("Type 'x' to go back")
        user_id = Validation.validate_id('User ID')
        # Initialize the User class
        user = User(self.user_db)

        # Find the user by ID to check if they exist
        existing_user = user.find_user_by_id(user_id)
        if existing_user:
            print(f"User found: {existing_user['Full Name']} (ID: {user_id})")

            # Show the fields that can be updated
            print("\nWhich field would you like to update?")
            print("1. Full Name")
            print("2. Address")
            print("3. Mobile Number")
            print("4. Email")
            print("5. Password")
            print("6. Cancel")
            choice = input("Enter the number corresponding to the field: ")
            new_value = None

            match choice:
                case '1':
                    new_value = Validation.check_input_name("New Full Name")
                    update_data = {'Full Name': new_value or existing_user['Full Name']}
                case '2':
                    new_value = self.get_address()
                    update_data = {'Address': new_value or existing_user['Address']}
                case '3':
                    new_value = Validation.check_input_mobile("New Mobile Number")
                    update_data = {'Mobile Number': new_value or existing_user['Mobile Number']}
                case '4':
                    new_value = Validation.check_input_email("New Email")
                    update_data = {'Email': new_value or existing_user['Email']}
                case '5':
                    new_value = Validation.check_input_password("New Password")
                    update_data = {'Password': new_value or existing_user['Password']}
                case '6':
                    print("Operation canceled. No updates made.")
                    return
                case _:
                    print("Invalid choice. Please select a valid option.")
                    return
            # Update the user
            user.update_user(user_id, update_data)
            # Print the update message based on the field updated
            if new_value is not None:
                print(f"User {new_value} (ID: {user_id}) updated successfully.\n")
        else:
            print(f"No user found with ID {user_id}.\n")


    # Customer Management Methods
    def add_corporate_customer(self):
        """
        Collect corporate customer data and add it to the system.
        """
        customer_id = self.generate_unique_id('C')
        company_name = Validation.check_company_city_country_name("Company Name")
        address = self.get_address()
        reference_person = Validation.check_input_name("Reference Person (User)")

        # Initialize the User class to access the user database
        user = User(self.user_db)
        # Find the reference person in the user database
        existing_user = user.find_user_by_name(reference_person)
        if not existing_user:
            print(f"Error: Reference Person '{reference_person}' not found in user database.")
            return

        invoice_email = Validation.check_input_email("Invoice Email")

        # Pack corporate customer data into a dictionary
        corporate_customer_data = {
            'ID': customer_id,
            'Company Name': company_name,
            'Company Address': address,
            'Reference Person': reference_person,
            'Reference Person Contact': f"{existing_user['Mobile Number']}, {existing_user['Email']}",
            'Invoice Email': invoice_email,
            'Related Users': existing_user['ID'],
        }

        corporate_customer = CorporateCustomer(self.corporate_customer_db, self.user_db)
        corporate_customer.add_customer(corporate_customer_data)
        print(f"Corporate customer {company_name} added successfully!\n")

    def remove_corporate_customer(self):
        """
        Remove a corporate customer from the system by their ID.
        """
        print("Type 'x' to go back")
        customer_id = Validation.validate_id("Customer ID")
        corporate_customer = CorporateCustomer(self.corporate_customer_db, self.user_db)

        try:
            corporate_customer.remove_customer(customer_id)
            print(f"Corporate customer with ID {customer_id} removed successfully.\n")
        except ValueError as e:
            print(e)

    def update_corporate_customer(self):
        """
        Update a corporate customer's information in the system by their ID.
        """
        print("Type 'x' to go back")
        customer_id = Validation.validate_id("Customer ID")
        corporate_customer = CorporateCustomer(self.corporate_customer_db, self.user_db)

        # Find the corporate customer by ID
        existing_customer = corporate_customer.find_customer_by_id(customer_id)
        if existing_customer:
            print(f"Corporate customer found: {existing_customer['Company Name']} (ID: {customer_id})")

            # Show the fields that can be updated
            print("\nWhich field would you like to update?")
            print("1. Company Name")
            print("2. Company Address")
            print("3. Reference Person")
            print("4. Invoice Email")
            print("5. Cancel")
            choice = input("Enter the number corresponding to the field: ")
            # Initialize a variable to hold the new value
            new_value = None

            match choice:
                case '1':
                    new_value = Validation.check_company_city_country_name("Company Name")
                    update_data = {'Company Name': new_value or existing_customer['Company Name']}
                case '2':
                    new_value = self.get_address()
                    update_data = {'Company Address': new_value or existing_customer['Company Address']}
                case '3':
                    new_value = Validation.check_input_name("New Reference Person")
                    user = User(self.user_db)
                    existing_user = user.find_user_by_name(new_value)
                    if existing_user:
                        # If the reference person is found, update the related fields
                        update_data = {
                            'Reference Person': new_value,
                            'Reference Person Contact': f"{existing_user['Mobile Number']}, {existing_user['Email']}",
                            'Related Users': existing_user['ID'],
                        }
                    else:
                        print(f"Error: Reference Person '{new_value}' not found in user database.")
                        return
                case '4':
                    new_value = Validation.check_input_email("Invoice Email")
                    update_data = {'Invoice Email': new_value or existing_customer['Invoice Email']}
                case '5':
                    print("Operation canceled. No updates made.")
                    return
                case _:
                    print("Invalid choice. Please select a valid option.")
                    return
            # Update the corporate customer
            corporate_customer.update_customer(customer_id, update_data)
            if new_value is not None:
                print(f"Corporate customer {existing_customer['Company Name']} (ID: {customer_id}) updated successfully.\n")
        else:
            print(f"No corporate customer found with ID {customer_id}.\n")


    # Private Customer Management Methods
    def add_private_customer(self):
        """
        Collect private customer data and add it to the system.
        """
        # Assuming you have a method to generate unique IDs
        customer_id = self.generate_unique_id('P')
        full_name = Validation.check_input_name("Full Name")
        address = self.get_address()
        mobile_number = Validation.check_input_mobile("Mobile Number")
        invoice_email = Validation.check_input_email("Invoice Email")

        # Pack private customer data into a dictionary
        private_customer_data = {
            'ID': customer_id,
            'Full Name': full_name,
            'Address': address,
            'Mobile Number': mobile_number,
            'Invoice Email': invoice_email,
        }

        private_customer = PrivateCustomer(self.private_customer_db)
        private_customer.add_customer(private_customer_data)
        print(f"Private customer {full_name} added successfully!\n")

    def remove_private_customer(self):
        """
        Remove a private customer from the system by their ID.
        """
        print("Type 'x' to go back")
        customer_id = Validation.validate_id("Customer ID")
        private_customer = PrivateCustomer(self.private_customer_db)

        try:
            private_customer.remove_customer(customer_id)
            print(f"Private customer with ID {customer_id} removed successfully.\n")
        except ValueError as e:
            print(e)

    def update_private_customer(self):
        """
        Update a private customer's information in the system by their ID.
        """
        print("Type 'x' to go back")
        customer_id = Validation.validate_id("Customer ID")
        private_customer = PrivateCustomer(self.private_customer_db)

        # Find the private customer by ID
        existing_customer = private_customer.find_customer_by_id(customer_id)
        if existing_customer:
            print(f"Private customer found: {existing_customer['Full Name']} (ID: {customer_id})")

            # Show the fields that can be updated
            print("\nWhich field would you like to update?")
            print("1. Full Name")
            print("2. Address")
            print("3. Mobile Number")
            print("4. Invoice Email")
            print("5. Cancel")
            choice = input("Enter the number corresponding to the field: ")
            # Initialize a variable to hold the new value
            new_value = None

            match choice:
                case '1':
                    new_value = Validation.check_input_name("Full Name")
                    update_data = {'Full Name': new_value or existing_customer['Full Name']}
                case '2':
                    new_value = self.get_address()
                    update_data = {'Address': new_value or existing_customer['Address']}
                case '3':
                    new_value = Validation.check_input_mobile("Mobile Number")
                    update_data = {'Mobile Number': new_value or existing_customer['Mobile Number']}
                case '4':
                    new_value = Validation.check_input_email("Invoice Email")
                    update_data = {'Invoice Email': new_value or existing_customer['Invoice Email']}
                case '5':
                    print("Operation canceled. No updates made.")
                    return
                case _:
                    print("Invalid choice. Please select a valid option.")
                    return
            # Update the private customer
            private_customer.update_customer(customer_id, update_data)
            if new_value is not None:
                print(f"Private customer {existing_customer['Full Name']} (ID: {customer_id}) updated successfully.\n")
        else:
            print(f"No private customer found with ID {customer_id}.\n")


    # Vehicle Management Methods
    def add_bike(self):
        """
        Add a new bike to the vehicle database.

        This method collects data about the bike, including its city, country, and capacity. 
        The bike has a maximum weight capacity of 10 kg and can carry up to 2 items. 
        The vehicle data is then added to the vehicle database, and the system confirms the bike addition.
        """
        vehicle_id = self.generate_unique_id('B')
        city = Validation.check_company_city_country_name('City')
        country = Validation.check_company_city_country_name('Country')
        current_position = Location(city, country)
        # Max weight for a bike
        max_capacity_weight = 10
        # Max item count for a bike
        max_capacity_items = 2
        # Pack bike data into a dictionary
        bike_data = {
            'Vehicle ID': vehicle_id,
            'Type': 'Bike',
            'Max Capacity (Weight)': max_capacity_weight,
            'Max Capacity (Item Count)': max_capacity_items,
            'Remaining Capacity (Weight)': max_capacity_weight,
            'Remaining Capacity (Item Count)': max_capacity_items,
            'Current Position': repr(current_position),
            'Status': 'free'
        }

        # Add bike data using the Vehicle class
        bike = Vehicle(self.vehicle_db)
        bike.add_vehicle(bike_data)
        print(f"Bike added successfully with ID {vehicle_id}!\n")

    def add_truck(self):
        """
        Add a new truck to the vehicle database.

        This method collects data about the truck, including its city, country, and capacity.
        The truck has a maximum weight capacity of 3000 kg and can carry up to 100 items. 
        The vehicle data is then added to the vehicle database, and the system confirms the truck addition.
        """
        vehicle_id = self.generate_unique_id('T')
        city = Validation.check_company_city_country_name('City')
        country = Validation.check_company_city_country_name('Country')
        current_position = Location(city, country)
        # Max weight for a truck
        max_capacity_weight = 3000
        # Max item count for a truck
        max_capacity_items = 100

        # Pack truck data into a dictionary
        truck_data = {
            'Vehicle ID': vehicle_id,
            'Type': 'Truck',
            'Max Capacity (Weight)': max_capacity_weight,
            'Max Capacity (Item Count)': max_capacity_items,
            'Remaining Capacity (Weight)': max_capacity_weight,
            'Remaining Capacity (Item Count)': max_capacity_items,
            'Current Position': repr(current_position),
            'Status': 'free'
        }

        # Add truck data using the Vehicle class
        truck = Vehicle(self.vehicle_db)
        truck.add_vehicle(truck_data)
        print(f"Truck added successfully with ID {vehicle_id}!\n")

    def add_ship(self):
        """
        Add a new ship to the vehicle database.

        This method collects data about the ship, including its city, country, and capacity.
        The ship has a maximum weight capacity of 100,000 kg and can carry up to 10,000 items. 
        The vehicle data is then added to the vehicle database, and the system confirms the ship addition.
        """
        vehicle_id = self.generate_unique_id('S')
        city = Validation.check_company_city_country_name('City')
        country = Validation.check_company_city_country_name('Country')
        current_position  = Location(city, country)
        # Max weight for a ship
        max_capacity_weight = 100000
        # Max item count for a ship
        max_capacity_items = 10000
        # Pack ship data into a dictionary
        ship_data = {
            'Vehicle ID': vehicle_id,
            'Type': 'Ship',
            'Max Capacity (Weight)': max_capacity_weight,
            'Max Capacity (Item Count)': max_capacity_items,
            'Remaining Capacity (Weight)': max_capacity_weight,
            'Remaining Capacity (Item Count)': max_capacity_items,
            'Current Position': repr(current_position),
            'Status': 'free'
        }

        # Add ship data using the Vehicle class
        ship = Vehicle(self.vehicle_db)
        ship.add_vehicle(ship_data)
        print(f"Ship added successfully with ID {vehicle_id}!\n")

    def remove_vehicles(self):
        """
        Remove a vehicle from the database by its Vehicle ID.
        Displays all vehicles and their current status before removal.
        Vehicles that are currently 'in_use' cannot be removed.
        """
        # Load vehicles from the database
        vehicles = self.vehicle_db.load_data()

        # Check if any vehicles are available
        if not vehicles:
            print("No vehicles available in the database.")
            return

        # Display all vehicles
        print(f"{'ID':<6} {'Type':<6} {'Remain Weight':<14} {'Remain Item':<13} {'Current Position':<25} {'Status':<8}")
        print("-" * 75)  # Separator line

        for vehicle in vehicles:
            vehicle_id = vehicle.get('Vehicle ID', 'Not Available')
            vehicle_type = vehicle.get('Type', 'Not Available')
            remaining_weight = vehicle.get('Remaining Capacity (Weight)', 'Not Available')
            remaining_items = vehicle.get('Remaining Capacity (Item Count)', 'Not Available')
            current_position = vehicle.get('Current Position', 'Not Available')
            status = vehicle.get('Status', 'Not Available')

            print(f"{vehicle_id:<6} {vehicle_type:<6} {remaining_weight:<14} {remaining_items:<13} {current_position:<25} {status:<8}")

        print("-" * 75)

        # Prompt for the Vehicle ID to remove
        print("Type 'x' to go back")
        vehicle_id = Validation.validate_id('Vehicle ID')

        # Create an instance of the Vehicle class
        vehicle_obj = Vehicle(self.vehicle_db)

        # Check if the vehicle exists in the loaded data
        vehicle_found = False
        for vehicle in vehicles:
            if vehicle.get('Vehicle ID') == vehicle_id:
                vehicle_found = True
                # Check if the vehicle is currently in use
                if vehicle.get('Status') == 'in_use':
                    print(f"Cannot remove vehicle with ID {vehicle_id} because it is currently in use.")
                    return
                try:
                    vehicle_obj.remove_vehicle(vehicle_id)
                    print(f"Vehicle with ID {vehicle_id} removed successfully.")
                except ValueError as e:
                    print(e)
                break
        if not vehicle_found:
            print(f"No vehicle found with ID {vehicle_id}.")


    # Create a shipment/order
    def add_order_shipment(self):
        """
        Create a new shipment or order and add it to the order database.

        This method gathers all the necessary details for creating a new order, including:

        1. Order ID Generation: A unique order ID prefixed with 'O' is generated.
        2. Order Priority: The user selects the order's priority (Low, Medium, or High).
        3. Customer Selection: The user chooses between a private or corporate customer and provides the relevant customer ID.
        4. Delivery Location: The user enters the delivery city and country, creating a `Location` object.
        5. Items: The user can add multiple items to the order. Item IDs are retrieved from the item database, and the total weight is calculated.
        6. Payment Details: The user inputs the payment method (e.g., credit card).
        7. Order Initialization: The order's status is set to "processing" and the order date is recorded.
        8. Database Storage: The order data, including customer, items, weight, and payment, is added to the order database.

        A confirmation message is displayed upon successful creation, showing the order ID and delivery date.

        Returns:
            None

        Raises:
            ValueError: If an invalid customer ID or item ID is entered.
        """
        order_id = self.generate_unique_id('O')
        priority = Validation.check_priority('Priority')

        # Select customer (either private or corporate)
        print("Select customer type:")
        print("1. Private Customer")
        print("2. Corporate Customer")
        customer_type_choice = input("Enter 1 or 2: ")

        if customer_type_choice == '1':
            customer_id = Validation.validate_id("Private Customer ID")
            # Create an instance of PrivateCustomer
            customer_obj = PrivateCustomer(self.private_customer_db)
        elif customer_type_choice == '2':
            customer_id = Validation.validate_id("Corporate Customer ID")
            # Create an instance of CorporateCustomer
            customer_obj = CorporateCustomer(self.corporate_customer_db, self.user_db)
        else:
            print("Invalid customer type choice.")
            return

        # Find the customer by ID using the respective method
        customer = customer_obj.find_customer_by_id(customer_id)
        if not customer:
            print(f"No customer found with ID {customer_id}.")
            return

        # Get delivery location (city and country)
        print("\n----- Enter Delivery Location -----")
        city = Validation.check_company_city_country_name("Delivery City")
        country = Validation.check_company_city_country_name("Delivery Country")
        delivery_location = repr(Location(city, country))

        # Get delivery dates
        delivery_date = Validation.get_delivery_date()

        # Save the order to the database with basic details first (without items)
        order_data = {
            'Order ID': order_id,
            'Priority': priority,
            'Customer': customer_id,
            'Delivery Location': delivery_location,
            'Payment Details': None,
            'Items': list(),
            'Total Weight': 0,
            'Order Status': 'processing',
            'Order Date': datetime.now(),
            'Delivery Date': delivery_date,
            'Vehicle': None
        }

        # Save the initial order to be able to find it when use add_item_to_order(order_id)
        order = Order(self.order_db)
        order.add_order(order_data)

        # Update items, payment...
        print("\n------ Adding items to the order ------\n")
        order_items= self.add_item_to_order(order_id)
        print(f"Order created successfully!\nID: {order_id}\nDelivery Date: {delivery_date}")
        if order_items is None:
            return


    def select_vehicle(self, total_weight, item_count, items_ids_and_quantities):
        """
        Select the appropriate vehicles based on total weight, item count, and specific item choice.
        :param total_weight: Total weight of items to be loaded.
        :param item_count: Total number of items to be loaded.
        :param item_choice: List of item IDs to be loaded.
        """
        # Load vehicles and items from the database
        vehicles = self.vehicle_db.load_data()
        items = self.item_db.load_data()

        # Sort vehicles based on their item capacity first and then by max weight
        vehicles.sort(key=lambda v: (int(v['Max Capacity (Item Count)']), float(v['Max Capacity (Weight)'])))
        remaining_weight = total_weight
        remaining_items = item_count
        updates = list()

        # Try to load selected items into vehicles one by one
        for vehicle_data in vehicles:
            if remaining_weight <= 0 and remaining_items <= 0:
                break

            # Access remaining capacities from the vehicle data
            remaining_weight_capacity = float(vehicle_data['Remaining Capacity (Weight)'])
            remaining_item_capacity = int(vehicle_data['Remaining Capacity (Item Count)'])
            vehicle_type = vehicle_data['Type']

            # Skip vehicles that are already full or in use
            if remaining_weight_capacity <= 0 or remaining_item_capacity <= 0 or vehicle_data['Status'] == 'in_use':
                continue
            # Loop through each item and its quantity
            for item_data in items_ids_and_quantities:
                # print(item_data)
                item_id = item_data['Item ID']
                quantity = item_data['Quantity']

                # Find the item details from the database
                item = next((i for i in items if i['ID'] == item_id), None)
                if not item:
                    continue

                item_weight = float(item['Weight'])
                item_type = item['Type']

                # Skip loading fragile items onto Bikes
                if vehicle_type == 'Bike' and item_type == 'fragile':
                    continue

                # Calculate how many items can be loaded based on both item and weight capacity
                max_items_by_capacity = min(remaining_items, remaining_item_capacity)
                max_weight_by_capacity = min(remaining_weight, remaining_weight_capacity)

                # Determine how many can be loaded based on both item and weight capacity
                loadable_items = min(quantity, max_items_by_capacity, int(max_weight_by_capacity / item_weight))

                if loadable_items > 0:
                    # Calculate the weight that can be loaded for the selected number of items
                    loadable_weight = loadable_items * item_weight

                    # Update the remaining counts
                    remaining_weight -= loadable_weight
                    remaining_items -= loadable_items
                    item_data['Quantity'] -= loadable_items

                    # Update the vehicle's remaining capacity for weight and items
                    remaining_weight_capacity -= loadable_weight
                    remaining_item_capacity -= loadable_items
                    # Prepare the update data
                    update_data = {
                        'Vehicle ID': vehicle_data['Vehicle ID'],
                        'Type': vehicle_data['Type'],
                        'Status': 'in_use',
                        'Remaining Capacity (Weight)': remaining_weight_capacity,
                        'Remaining Capacity (Item Count)': remaining_item_capacity
                    }
                    # Update the vehicle in the database using its ID
                    vehicle_instance = Vehicle(self.vehicle_db)
                    vehicle_instance.update_vehicle(vehicle_data['Vehicle ID'], update_data)
                    print(f"\n{vehicle_data['Vehicle ID']} - {vehicle_data['Type']} loaded with {loadable_items} item (ID: {item_id}), Total weight: {loadable_weight:.2f} kg.")
                    # Append the update data for this vehicle to the list
                    updates.append(update_data)
        if remaining_items > 0:
            print("Not enough vehicle capacity to load all items!")

        # Return the list of all update data
        return updates


    # Items Management Methods
    def add_item_to_database(self):
        """
        Collect item data and add it to the item database.
        """
        # Generate a unique ID for the item
        item_id = self.generate_unique_id('I')

        # Collect information about the item from the user
        price_per_kg = Validation.check_positive_float("Price per kg")
        weight = Validation.check_positive_float("Weight (in kg)")
        item_type = Validation.check_item_type("Item type")

        # Pack item data into a dictionary
        item_data = {
            'ID': item_id,
            'Price per kg': price_per_kg,
            'Weight': weight,
            'Type': item_type
        }

        # Create an instance of the Item class and add the item to the database
        item = Item(self.item_db)
        item.add_item(item_data)
        print(f"Item added successfully with ID {item_id}!\n")

    def add_item_to_order(self, order_id):
        """
        Add an item to an existing order in the order database.
        """
        # Find the order by its ID in the order database
        order = Order(self.order_db)
        order_data = order.find_order_by_id(order_id)

        if not order_data:
            print(f"No order found with ID {order_id}.")
            # No order found, so return None for items and 0 for weight
            return None, 0

        # Load existing items from the item database
        items_data = self.item_db.load_data()
        if not items_data:
            print("No items available in the database.")
            return None, 0

        # Display available items
        print("\n---- Available Items in the Database ----\n")
        for item in items_data:
            # Safely access the item fields and handle missing fields
            item_id = item.get('ID', 'Not Available')
            price_per_kg = item.get('Price per kg', 'Not Available')
            weight = item.get('Weight', 'Not Available')
            item_type = item.get('Type', 'Not Available')

            # Display item details
            print(f"ID: {item_id}, Price per KG: {price_per_kg}, Weight: {weight}, Type: {item_type}")

        # Initialize an empty list to store selected items
        order_items = list()
        print('You can now enter one or more item(s)')

        # Loop for selecting multiple items
        while True:
            item_choice = Validation.validate_id("item ID you want to order (or type 'x' to finish)")
            if item_choice.lower() == 'x':
                break

            items_obj = Item(self.item_db)
            selected_item = items_obj.find_item_by_id(item_choice)

            if not selected_item:
                print(f"No item found with ID {item_choice}.")
                continue

            # Ask how many of the selected item are needed
            quantity = Validation.check_positive_integer("Enter the number of items needed for this order")

            # Calculate total weight for the selected item
            item_weight = quantity * float(selected_item['Weight'])

            # Prepare selected item data that would be send to order.csv
            new_item = {'Item ID': selected_item['ID'],
                        'Quantity': quantity,
                        'Weight': item_weight,
                        'Price per kg': selected_item['Price per kg']}

            # Append the new item to the order items list
            order_items.append(new_item)

        # Calculate the new total weight
        total_weight = sum(item['Weight'] for item in order_items)
        new_total_weight = float(order_data['Total Weight']) + total_weight

        # Select a vehicle for the delivery
        total_item_count = sum(item['Quantity'] for item in order_items)
        # Prepare the list of item IDs and quantities for select_vehicle
        items_ids_and_quantities = [{'Item ID': item['Item ID'], 'Quantity': item['Quantity']} for item in order_items]

        vehicle = self.select_vehicle(total_weight, total_item_count, items_ids_and_quantities)

        # Parse the existing vehicles from the order
        order_vehicles = eval(order_data['Vehicle']) if order_data['Vehicle'] else list()

        # Append the new vehicle to the order vehicles if vehicle is valid
        if vehicle:
            order_vehicles.append(vehicle)

        # Create and validate payment details
        print("\n----- Enter Payment Details -----\n")
        transaction_id = self.generate_unique_id('TR')
        payment_method = Validation.check_payment_method('Payment Method')
        currency = Validation.check_currency('Currency')

        # Calculate amount for all selected items
        total_amount = sum(quantity * float(selected_item['Price per kg']) for selected_item, quantity in zip(order_items, [item['Quantity'] for item in order_items]))
        print(f'\nThe total amount for your order is: {total_amount} {currency}\n')

        payment_status = Validation.check_payment_status('Payment Status')

        # Gather card information if applicable
        card_info = Validation.check_card_info("Card Information")

        # Create the payment details object
        payment_details_data = {
            'Payment Method': payment_method,
            'Transaction ID': transaction_id,
            'Currency': currency,
            'Amount': total_amount,
            'Payment Status': payment_status,
            'Card Information': card_info
        }
        payment_details = Payment(self.payment_db)
        payment_details.add_payment(payment_details_data)
        print(f"Payment details with id {transaction_id} added!")

        # Prepare the updated order data
        update_data = {
            'Payment Details': payment_details_data,
            'Items': order_items,
            'Total Weight': new_total_weight,
            'Vehicle': order_vehicles
        }

        # Update the order in the database with the new items, total weight, and vehicle
        order.update_order(order_id, update_data)
        return

    def remove_items(self):
        """
        Remove an item from the database by its ID.
        Displays all items and their current status before removal.
        """
        # Load items from the database
        items = self.item_db.load_data()

        # Check if any items are available
        if not items:
            print("No items available in the database.")
            return

        # Display all items
        print(f"{'ID':<6} {'Price per kg':<14} {'Weight':<8} {'Type':<6}")
        print("-" * 40)

        for item in items:
            item_id = item.get('ID', 'Not Available')
            price_per_kg = item.get('Price per kg', 'Not Available')
            weight = item.get('Weight', 'Not Available')
            item_type = item.get('Type', 'Not Available')

            print(f"{item_id:<8} {price_per_kg:<12} {weight:<8} {item_type:<6}")

        print("-" * 40)

        # Prompt for the item ID to remove
        print("Type 'x' to go back")
        item_id = Validation.validate_id('Item ID')

        # Create an instance of the Item class
        item_obj = Item(self.item_db)

        # Check if the item exists in the loaded data
        item_found = False
        for item in items:
            if item.get('ID') == item_id:
                item_found = True
                try:
                    item_obj.remove_item(item_id)
                    print(f"Item with ID {item_id} removed successfully.")
                except ValueError as e:
                    print(e)
                break

        if not item_found:
            print(f"No item found with ID {item_id}.")


    # Retrieve and update the status of an order
    def update_order_status(self):
        """
        Update the status of an existing order in the order database.
        The user is prompted for the Order ID, and then the status can be changed to 
        'processing', 'delivered', or 'canceled'.
        If the status is updated to 'delivered',
        the vehicle's current position is updated based on the delivery location,
        and its status and capacity are reset for future use.

        If the status is updated to 'canceled',
        the vehicle's status is reset to 'free'
        and capacities are reset without changing the position.
        """
        # Load existing orders from the database
        orders = self.order_db.load_data()

        # Display the current status of all orders
        print("\nCurrent Orders and Status:")
        for order_data in orders:
            order_id = order_data['Order ID']
            current_status = order_data['Order Status']
            print(f"Order ID: {order_id}, Status: {current_status}")

        # Prompt for the Order ID
        print("Type 'x' to go back")
        order_id = Validation.validate_id("Order ID")

        # Create an instance of the Order class
        order = Order(self.order_db)
        order_data = order.find_order_by_id(order_id)

        if not order_data:
            print(f"No order found with ID {order_id}.")
            return

        # Prompt for the new status
        new_status = Validation.check_order_status('New Status')

        # If the new status is 'delivered', update the vehicle's current position
        if new_status == 'delivered':
            delivery_location = order_data['Delivery Location']

            # Convert the 'Vehicle' field back to a list using eval
            vehicles_in_order = eval(order_data['Vehicle'])

            # Iterate over each vehicle in the list
            for vehicle_entry in vehicles_in_order:
                # Check if the vehicle entry is itself a list
                if isinstance(vehicle_entry, list):
                    # If it's a nested list, loop through each vehicle within that list
                    for nested_vehicle in vehicle_entry:
                        # Call the update_vehicle_status method to update
                        self.update_vehicle_status(nested_vehicle, delivery_location)
                else:
                    # If it's not a nested list, directly update
                    self.update_vehicle_status(vehicle_entry, delivery_location)

        # If the new status is 'canceled', reset vehicle status and capacity without updating position
        elif new_status == 'canceled':
            vehicles_in_order = eval(order_data['Vehicle'])
            # Same idea here
            for vehicle_entry in vehicles_in_order:
                if isinstance(vehicle_entry, list):
                    for nested_vehicle in vehicle_entry:
                        self.reset_vehicle_status(nested_vehicle)
                else:
                    self.reset_vehicle_status(vehicle_entry)

        # Prepare the update data for the order
        update_data = {
            'Order Status': new_status
        }
        # Update the order in the database
        order.update_order(order_id, update_data)
        print(f"\nOrder {order_id} status updated successfully to '{new_status}'.\n")

    def update_vehicle_status(self, vehicle_entry, delivery_location):
        """
        Update the vehicle's current position and reset its capacity and status.

        :param vehicle_entry: Dictionary containing vehicle data.
        :param delivery_location: The new delivery location to update the vehicle's position.
        """
        vehicle_id = vehicle_entry['Vehicle ID']

        # Find the vehicle by its ID
        vehicle_instance = Vehicle(self.vehicle_db)
        vehicle_data = vehicle_instance.find_vehicle_by_id(vehicle_id)

        if vehicle_data:
            # Reset remaining capacity to max values and update current position and status
            update_vehicle_data = {
                'Current Position': delivery_location,
                'Status': 'free',  # Mark the vehicle as free for future use
                'Remaining Capacity (Weight)': vehicle_data['Max Capacity (Weight)'],  # Reset weight capacity
                'Remaining Capacity (Item Count)': vehicle_data['Max Capacity (Item Count)']  # Reset item capacity
            }

            # Update the vehicle's current position and capacities in the vehicle database
            vehicle_instance.update_vehicle(vehicle_id, update_vehicle_data)
            print(f"\nVehicle ID: {vehicle_id}\nNew position: {delivery_location}\nStatus: free, and capacities reset.")
        else:
            print(f"No vehicle found with ID {vehicle_id}.")

    def reset_vehicle_status(self, vehicle_entry):
        """
        Reset the vehicle's status and capacity when the order is canceled.

        :param vehicle_entry: Dictionary containing vehicle data.
        """
        vehicle_id = vehicle_entry['Vehicle ID']

        # Find the vehicle by its ID
        vehicle_instance = Vehicle(self.vehicle_db)
        vehicle_data = vehicle_instance.find_vehicle_by_id(vehicle_id)

        if vehicle_data:
            # Reset only the status and capacity
            update_vehicle_data = {
                'Status': 'free',  # Mark the vehicle as free for future use
                'Remaining Capacity (Weight)': vehicle_data['Max Capacity (Weight)'],  # Reset weight capacity
                'Remaining Capacity (Item Count)': vehicle_data['Max Capacity (Item Count)']  # Reset item capacity
            }

            # Update the vehicle's status and capacities in the vehicle database
            vehicle_instance.update_vehicle(vehicle_id, update_vehicle_data)
            print(f"Vehicle ID: {vehicle_id}\nStatus: free and capacities reset.")
        else:
            print(f"No vehicle found with ID {vehicle_id}.")


    # Retrieve and update the payment status
    def update_payment_status(self):
        """
        Display all payments, prompt for Transaction ID, and update the payment status.
        """
        # Load payments from the CSV file
        payments = self.payment_db.load_data()

        # Display all payments and their statuses
        print("\n--- All Payments and Statuses ---")
        for payment_data in payments:
            transaction_id = payment_data['Transaction ID']
            current_status = payment_data['Payment Status']
            print(f"Transaction ID: {transaction_id}, Status: {current_status}")

        # Prompt user for the Transaction ID
        print("Type 'x' to go back")
        transaction_id = Validation.validate_transaction_id('Transaction ID')

        # Create an instance of the Payment class and find the payment by ID
        payment = Payment(self.payment_db)
        payment_data = payment.find_payment_by_id(transaction_id)

        # If no payment found, exit
        if not payment_data:
            print(f"No payment found with ID {transaction_id}.")
            return

        # Display current payment status
        current_status = payment_data['Payment Status']
        print(f"\nCurrent Payment Status for Transaction ID {transaction_id}: {current_status}")

        # Prompt user for the new payment status
        new_status = Validation.check_payment_status('New Status')

        # Prepare updated data
        update_data = {
            'Payment Status': new_status
        }

        # Update the payment status in the CSV file
        payment.update_payment(transaction_id, update_data)
        print(f"\nPayment status updated for Transaction ID {transaction_id} to '{new_status}'.\n")


    # login Management Methods
    def login(self):
        """
        Log in the user by validating the username (full name) and password.
        Allows up to 3 attempts before locking out.
        """
        print('\n----- Enter User Name and Password to login -----\n')
        # Get user input for full name
        full_name = Validation.check_input_name("User Name")

        # Initialize the User class and find the user by name
        user = User(self.user_db)
        user_data = user.find_user_by_name(full_name)

        # Check if the user was found
        if not user_data:
            print(f"No user found with the name '{full_name}'!\n")
            return False, None

        # Allow up to 3 attempts for password entry
        for attempt in range(3):  # Using a for loop for better readability
            # Get user input for password
            password = Validation.check_input_password("Password")

            # Validate the password
            if password == user_data['Password']:
                print(f"Login successful!\n\nHello, {user_data['Full Name']}!\n")
                return True, full_name

            remaining_attempts = 2 - attempt  # Calculate remaining attempts
            print(f"Invalid password. Please try again.\nYou have {remaining_attempts} attempt(s) left.\n")

        # If all attempts are used
        print("You have exceeded the maximum number of attempts.\nLogin failed.\n")
        return False, None

    def check_for_users(self):
        """
        Check if there are users in the 'user.csv' file.
        If no users are found, print an appropriate message.
        """
        # Load the data from user.csv
        users = self.user_db.load_data()

        # Check if the file is empty or if there are no users
        if users:
            return
        print("\nNo users found in database.\nAdd a user to login and use the system.\n")
        self.add_user_main()
        self.welcome_message()

    def log_file(self, full_name):
        """
        the user who logged in along with the timestamp.
        """
        try:
            # Get the current timestamp
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Open the log file in append mode and write the log
            with open('log.txt', 'a', encoding='utf-8') as file:
                file.write(f'User: {full_name} - Login Time: {current_time}\n')
        except Exception as e:
            raise e


    # Main menu Methods
    @staticmethod
    def welcome_message():
        """
        Display a welcome message to the user.
        Since it doesn't need to access instance data, it is defined as a @staticmethod.

        This method is called at the start of the application to greet the user and introduce 
        the logistics system. It does not require any input or return a value.
        """
        print("Welcome to the Logistics System!")
        print("\nThis system allows you to manage users, vehicles, orders, and payments efficiently."
              "\nBelow is a quick guide to help you get started:")
        print("""
    1. User Management: Add, remove, or update user details including
        their ID, full name, address, mobile number, and email.

    2. Customer Management: Handle both corporate and private customers,
        including adding, removing, or updating customer information
        and managing related user details.

    3. Vehicle Management: Add different types of vehicles, such as
        bikes, trucks, or ships, to the system. You can also
        update vehicle capacities and assign them to deliveries
        based on item weight and count.

    4. Order Creation: Create new shipment orders by
        specifying delivery locations, payment details, and selecting vehicles
        for delivery based on the shipment size and weight.

    5. Item Management: Add or remove items in a shipment or the item database.
        Items are categorized by price per kilogram,
        weight, and type (e.g., fragile or solid).

    6. Payment Processing: Manage payments by adding new payment details,
        updating payment statuses (e.g., paid or unpaid),
        and checking payment information for each transaction.

    7. Status Tracking: Track and update the status of orders from
        Processing' to 'Delivered' or 'Canceled' as needed.

    Please log in to continue and access the system.\n\n\n
********NOTE: ADD ITEMS AND VEHICLES BEFORE CREATE ANY ORDER.********
        """)

    @staticmethod
    def main_menu():
        """
        Display the main menu for the logistics system.

        This method presents the main options available in the system, such as user management, 
        vehicle management, shipment/order creation, item management, and payment/status updates. 
        The user is prompted to select an option to proceed.
        """
        print('\n' + '-' * 16 + ' Main Menu ' + '-' * 16)
        print("1. Add/Remove/Update a User in the System")
        print("2. Add/Remove/Update a Corporate Customer")
        print("3. Add/Remove/Update a Private Customer")
        print("4. Vehicle Management")
        print("5. Create a Shipment/Order")
        print("6. Item Management")
        print("7. Display/Update Order and Payment Status")
        print("8. Exit")

    @staticmethod
    def vehicle_management_menu():
        """
        Display the vehicle management menu.

        This method presents options for managing vehicles in the system, such as adding a bike, 
        truck, or ship. The user is prompted to select a specific vehicle type to add to the system.
        """
        print("\n--- Vehicle Management Menu ---")
        print("1. Add a Bike")
        print("2. Add a Truck")
        print("3. Add a Ship")
        print("4. Display/Remove a Vehicles")
        print("5. Go back to the Main Menu")

    @staticmethod
    def user_management_menu():
        """
        Display the user management menu.

        This method provides options for managing users in the system, such as adding, removing, 
        or updating a user. The user is prompted to select the desired user management action.
        """
        print('\n' + '-' * 5 + ' User Management Menu ' + '-' * 5)
        print("1. Add User in the System")
        print("2. Remove User in the System")
        print("3. Update User in the System")
        print("4. Back to Main Menu")

    @staticmethod
    def item_management_menu():
        """
        Display the item management menu.

        This method provides options for managing items in the system, such as adding or removing items. 
        The user can choose to add new items to the shipment or to the item database.
        """
        print("\n--- Item Management Menu ---")
        print("1. Add Items to a Database")
        print("2. Add item to an Order")
        print("3. Display/Remove Items")
        print("4. Go back to the Main Menu")

    @staticmethod
    def status_management_menu():
        """
        Display the status management submenu for updating order and payment statuses.
        """
        print("\n--- Status Management Menu ---")
        print("1. Display/Update Order Status")
        print("2. Display/Update Payment Status")
        print("3. Go back to the Main Menu")

    @staticmethod
    def corporate_customer_management_menu():
        """
        Display the corporate customer management menu.

        This method provides options for managing corporate customers in the system, 
        such as adding, removing, or updating a corporate customer.
        """
        print('\n' + '-' * 5 + ' Corporate Customer Management Menu ' + '-' * 5)
        print("1. Add Corporate Customer")
        print("2. Remove Corporate Customer")
        print("3. Update Corporate Customer")
        print("4. Back to Main Menu")

    @staticmethod
    def private_customer_management_menu():
        """
        Display the private customer management menu.

        This method provides options for managing private customers in the system, 
        such as adding, removing, or updating a private customer.
        """
        print('\n' + '-' * 5 + ' Private Customer Management Menu ' + '-' * 5)
        print("1. Add Private Customer")
        print("2. Remove Private Customer")
        print("3. Update Private Customer")
        print("4. Back to Main Menu")

    def run(self):
        """
        Run the main application loop.

        This method continuously displays the main menu and handles user input for selecting options.
        It manages the overall flow of the application, calling the appropriate methods 
        based on the user's selection.
        """
        while True:
            self.main_menu()
            choice = input("\nChoose an option (1-8): ")

            match choice:
                case "1":
                    # Show user management submenu
                    self.user_management_menu()
                    user_choice = input("Choose an option (1-4): ")

                    match user_choice:
                        case "1":
                            self.add_user_main()
                        case "2":
                            self.remove_user_main()
                        case "3":
                            self.update_user_main()
                        case "4":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "2":
                    # Show corporate customer submenu
                    self.corporate_customer_management_menu()
                    corporate_choice = input("Choose an option (1-4): ")

                    match corporate_choice:
                        case "1":
                            self.add_corporate_customer()
                        case "2":
                            self.remove_corporate_customer()
                        case "3":
                            self.update_corporate_customer()
                        case "4":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "3":
                    # Show private customer submenu
                    self.private_customer_management_menu()
                    private_choice = input("Choose an option (1-4): ")

                    match private_choice:
                        case "1":
                            self.add_private_customer()
                        case "2":
                            self.remove_private_customer()
                        case "3":
                            self.update_private_customer()
                        case "4":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "4":
                    # Show vehicle management submenu
                    self.vehicle_management_menu()
                    vehicle_choice = input("Choose an option (1-5): ")

                    match vehicle_choice:
                        case "1":
                            self.add_bike()
                        case "2":
                            self.add_truck()
                        case "3":
                            self.add_ship()
                        case "4":
                            self.remove_vehicles()
                        case "5":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "5":
                    self.add_order_shipment()

                case "6":
                    # Show item management submenu
                    self.item_management_menu()
                    item_choice = input("Choose an option (1-4): ")

                    match item_choice:
                        case "1":
                            self.add_item_to_database()
                        case "2":
                            print("Type 'x' to go back")
                            # Prompt for the Order ID and add the item to an existing order
                            order_id = Validation.validate_id("Order ID")
                            # Add the item to an existing order
                            self.add_item_to_order(order_id)
                        case "3":
                            self.remove_items()
                        case "4":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "7":
                    # Show status management submenu
                    self.status_management_menu()
                    status_choice = input("Choose an option (1-3): ")

                    match status_choice:
                        case "1":
                            self.update_order_status()
                        case "2":
                            self.update_payment_status()
                        case "3":
                            continue
                        case _:
                            print("Invalid choice, please try again.")

                case "8":
                    print("Exiting the system...\n")
                    break
                case _:
                    print("Invalid choice, please try again.")
