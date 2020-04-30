# This module is used to compute the fare to be paid by a Customer


class FareCalculation():
    """
    Contains config-related variables and functions
    """
    DEFAULT_BASE_FARE = 3

    def __init__(self):
        self.default_base_fare = 3  # default base fare

    def set_default_fare(self, value):
        """
        Updates the default base fare config
        based on the passed value
        """
        self.default_base_fare = value

    def get_fare(self, seats):
        """
        Calculates and returns the fare based on the
        seats reserved by the customer
        """
        fare = self.default_base_fare * seats

        return fare
