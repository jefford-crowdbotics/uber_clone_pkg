# This module contains information about a Booking/Trip
import random

from .lib.pyroutelib2.models.route import Router
from .lib.pyroutelib2.models.loadOsm import LoadOsm


# Initializing map data
MAP_DATA = LoadOsm("car")
MAX_SEATS = 3


class TripConfig():
    """
    Holds variables and data for configurations
    relating to a Booking/Trip
    """

    def __init__(self):
        """
        Default values for configuration
        """
        self.base_fare = 3
        self.max_seats = MAX_SEATS
        self.response_time = 60
        self.process_time = 180
        self.max_radius = 1

    def set_base_fare(self, value):
        """
        Update the value of the default base fare
        Params:
            value - int
        """
        if isinstance(value, (int, float)):
            self.base_fare = value
        else:
            raise Exception("Invalid parameter type. Function"
                            "should only receive integer/float values")

    def set_max_seats(self, value):
        """
        Update the value of the default max seats
        Params:
            value - int
        """
        if isinstance(value, int):
            self.max_seats = value
        else:
            raise Exception("Invalid parameter type. Function"
                            "should only receive integer values")

    def set_response_time(self, value):
        """
        Update the value of the default response time
        Params:
            value - int
        """
        if isinstance(value, (int, float)):
            self.response_time = value
        else:
            raise Exception("Invalid parameter type. Function"
                            "should only receive integer/float values")

    def set_process_time(self, value):
        """
        Update the value of the default process time
        Params:
            value - int
        """
        if isinstance(value, (int, float)):
            self.process_time = value
        else:
            raise Exception("Invalid parameter type. Function"
                            "should only receive integer/float values")
    
    def set_max_radius(self, value):
        """
        Update the value of the default max radius
        Params:
            value - int/float
        """
        if isinstance(value, (int, float)):
            self.max_radius = value
        else:
            raise Exception("Invalid parameter type. Function"
                            "should only receive integer/float values")


class Trip():
    """
    Holds information about a trip
    """

    def __init__(self, config, rider, start_node, end_node,
                 seats_reserved, fare=0, driver=False):
        """
        Params:
            config, driver, rider   - objects
            start_node, end_node    - latitude and longitude tuple values
            seats_reserved, fare    - float/int values
        """
        self.config = config
        self.driver = driver
        self.rider = rider
        self.start_node = start_node  # pickup location
        self.end_node = end_node  # drop off location
        self.seats_reserved = seats_reserved
        self.fare = fare

    def get_fare(self):
        """
        Computes the fare of the trip
        Params:
            self - an instance of a trip
        """
        fare = self.config.base_fare * self.seats_reserved

        return fare

    def get_node(self, latitude, longitude):
        """
        Convert a pair of lat/long values to a node
        """
        return MAP_DATA.findNode(latitude, longitude)

    def get_route(self, start_coord, end_coord):
        """
        Returns a list of nodes that passes the route
        Params:
            start_coord, end_coord - tuple values (lat/long)
        """
        start_node = MAP_DATA.findNode(start_coord[0], start_coord[1])
        end_node = MAP_DATA.findNode(end_coord[0], end_coord[1])

        router = Router(MAP_DATA)
        result, route = router.doRoute(start_node, end_node)
        if result == 'success':
            # display the nodes
            # print(route)

            # list the lat/long
            # for item in route:
            #     node = MAP_DATA.rnodes[item]
            #     print("%d: %f,%f" % (item, node[0], node[1]))

            return route
        else:
            print("Failed to identify route (%s)" % result)
            return False
    
    def _filter_by_match(self, driver):
        """
        A utility function to filter drivers with 
        matching trips. Used in filter() call
        Params:
            self - an instance of trip
            driver - driver instance from the list
        """
        # Note that we are using the active route of the Driver
        # from his realtime location to current destination
        driver_current_route = self.get_route(
            driver.current_location,
            driver.current_trip.end_node
        )

        # Check the route of the current trip and see if the list of route
        # is a sublist of the driver current route
        current_trip_route = self.get_route(
            self.start_node,
            self.end_node
        )

        # Removing the last node from the current trip, 
        # since it could mean a minor detour node
        current_trip_route = current_trip_route[:len(current_trip_route) - 1]

        if(all(node in driver_current_route for node in current_trip_route)):
            return True
        else:
            return False
    
    def _filter_by_distance(self, driver):
        """
        A utility function to filter drivers with 
        that are within a set radius. Used in filter() call
        Params:
            self - an instance of trip
            driver - driver instance from the list
        """
        # Distance is in km
        driver_distance = driver.get_distance(
            self.start_node[0],
            self.start_node[1]
        )

        if driver_distance <= self.config.max_radius:
            return True
        else:
            return False

    
    def _sort_by_distance(self, driver):
        """
        A utility function to get the distance of a driver.
        Used as a custom sorting key in sorted() function
        Params:
            self - an instance of a trip
            driver - driver instance from the list
        """
        return driver.get_distance(
            self.start_node[0],
            self.start_node[1]
        )

    def get_available_drivers(self, drivers, is_sorted=True):
        """
        Select a matching driver based on the list of drivers
        Params:
            self - an instance of trip
            drivers - list of Driver objects
            is_sorted - flag to return a sorted list or not
        Returns:
            A list of driver objects
        """
        trip = self

        # filter online drivers
        online_drivers = self.get_online_drivers(drivers)

        # find matching drivers - drivers with ongoing trip
        active_drivers = list(filter(
            lambda driver: driver.current_trip,
            online_drivers
        ))
        matching_drivers = list(filter(trip._filter_by_match, active_drivers))

        # if there are matching drivers, select from that list
        if matching_drivers:
            # filter matching drivers by available seats
            available_drivers = list(filter(
                lambda driver: driver.available_seats >= trip.seats_reserved,
                matching_drivers
                ))
        else:  # just select the closest driver with no ongoing trip
            available_drivers = self.get_idle_drivers(online_drivers)

        if is_sorted:
            return self.get_sorted_drivers(available_drivers)
        else:
            return available_drivers

    def get_sorted_drivers(self, drivers):
        """
        Sort the list of drivers by distance
        """
        sorted_drivers = sorted(drivers, key=self._sort_by_distance)

        return sorted_drivers

    def get_online_drivers(self, drivers):
        """
        Filters the list of drivers with is_online = True
        """
        # filter online drivers
        online_drivers = list(filter(
            lambda driver: driver.is_online,
            drivers
        ))

        return online_drivers

    def get_nearby_drivers(self, drivers):
        """
        Returns a list of drivers that are within a set radius
        Params:
            self - an instance of a trip
        """
        nearby_drivers = list(filter(self._filter_by_distance, drivers))

        return nearby_drivers

    def get_idle_drivers(self, drivers):
        """
        Return online drivers with no ongoing trip that are
        within the set radius
        Assumption:
            Drivers in the list are online
        """
        nearby_drivers = self.get_nearby_drivers(drivers)
        idle_drivers = list(filter(
            lambda driver: not driver.current_trip,
            nearby_drivers
        ))

        return idle_drivers
