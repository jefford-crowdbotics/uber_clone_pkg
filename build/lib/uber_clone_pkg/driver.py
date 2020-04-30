import geopy.distance

from .trip import MAX_SEATS


class Driver:
    """
    Holds information about a Driver
    """

    def __init__(self, unique_id, current_location, is_online,
                 available_seats=MAX_SEATS, current_trip=False):
        """
        Params:
            current_trip            - object
            available_seats         - int value
            current_location        - tuple (lat/long) value
        """
        self.unique_id = unique_id
        self.current_location = current_location
        self.is_online = is_online
        self.available_seats = available_seats
        self.current_trip = current_trip

    def get_distance(self, latitude, longitude):
        """
        Calculate and returns the distance of a driver from its
        current location to a target coordinates.
        Params:
            * self - an instance of a driver
            * lat, long - latitude and longitude values
        Notes:
            * Uses the geopy library to compute for distance
            * Sample link to verify distance: https://www.geodatasource.com/distance-calculator
        """
        target_coordinates = (latitude, longitude)
        driver_coordinates = (
            self.current_location[0],
            self.current_location[1]
        )

        distance = geopy.distance.vincenty(target_coordinates, driver_coordinates).km

        return distance
