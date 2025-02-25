"""
location.py - Module for Managing Location Data

This module defines the Location class, which represents a geographical
location with attributes for city and country.
"""

class Location:
    """
    Location class to represent a geographical location.

    Attributes:
        city (str): The city of the location.
        country (str): The country of the location.
    """
    def __init__(self, city: str, country: str) -> None:
        self.city = city
        self.country = country

    def __repr__(self) -> str:
        """Return a string representation of the Location object."""
        return f"{self.city}/{self.country}"
    