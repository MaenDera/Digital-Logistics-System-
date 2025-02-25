"""
address.py - Module for Address Management

This module defines the Address class, which represents a postal address
with attributes for street, building number, zip code, and city.
"""

class Address:
    """
    Address class to represent a postal address.

    Attributes:
        street (str): The street name of the address.
        building_nr (int): The building number of the address.
        zip_code (int): The postal code for the address.
        city (str): The city of the address.
    """
    def __init__(self, street:str,
                 building_nr:int,
                 zip_code:int,
                 city:str) -> None:
        self.street = street
        self.building_nr =building_nr
        self.zip_code =zip_code
        self.city = city

    def __repr__(self) -> str:
        return (f"St:{self.street} - Build#:{self.building_nr} - "
                f"ZC: {self.zip_code} - Cty: {self.city}")
    