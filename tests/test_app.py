import time
from random import randint

from uber_clone_pkg import (
    Trip,
    TripConfig,
    Driver
)

##### Initialize Trip Config #####
TRIP_CONFIG = TripConfig()
# Override config defaults
# TRIP_CONFIG.set_base_fare(5)

##### Initialize Trip Instances #####

# Trip to Match - 1
TRIP_TO_MATCH_1 = Trip(
    config=TRIP_CONFIG,
    rider=False,
    start_node=(7.0495, 125.5907),
    end_node=(7.0517, 125.5903),
    seats_reserved=2,
)

# Trip to Match - 2
TRIP_TO_MATCH_2 = Trip(
    config=TRIP_CONFIG,
    rider=False,
    start_node=(7.0739938, 125.6126872),
    end_node=(7.0753224, 125.6132193),
    seats_reserved=2,
)

# Matching Trip (SM to Gaisano)
# Sample route: https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=7.0493%2C125.5885%3B7.0777%2C125.6140#map=15/7.0632/125.6002
TRIP_MATCHING = Trip(
    config=TRIP_CONFIG,
    rider=False,
    start_node=(7.0493, 125.5885),
    end_node=(7.0777, 125.6140),
    seats_reserved=2,
)

# Mismatching Trip - 1
TRIP_MISMATCHING_1 = Trip(
    config=TRIP_CONFIG,
    rider=False,
    start_node=(7.0581343, 125.5685814),
    end_node=(7.0571582, 125.5721307),
    seats_reserved=1,
)

# Mismatching Trip - 2
TRIP_MISMATCHING_2 = Trip(
    config=TRIP_CONFIG,
    rider=False,
    start_node=(7.0606491, 125.5640547),
    end_node=(7.0619090, 125.5611702),
    seats_reserved=1,
)

##### Initialize Driver Instances #####
## This is a list where we can select a
## driver to assign for our trip to match
DRIVERS = []

# SM Ecoland -> Gaisano Bajada (Matching Driver) - can accommodate MATCHING_TRIPS
MATCHING_DRIVER = Driver(
    unique_id=randint(1000, 9999),
    current_location=(7.0491888, 125.5893258),
    is_online=True,
    available_seats=4,
    current_trip=TRIP_MATCHING
)

# Other Drivers (Mismatching Drivers)
MISMATCHING_DRIVER_1 = Driver(
    unique_id=randint(1000, 9999),
    current_location=(7.0649960, 125.6017195),
    is_online=True,
    available_seats=4,
    current_trip=TRIP_MISMATCHING_1
)

MISMATCHING_DRIVER_2 = Driver(
    unique_id=randint(1000, 9999),
    current_location=(7.0649960, 125.6017195),
    is_online=True,
    available_seats=4,
    current_trip=TRIP_MISMATCHING_2
)

# Idle drivers
IDLE_DRIVER_1 = Driver(
    unique_id=randint(1000, 9999),
    current_location=(7.0649960, 125.6017195),
    is_online=True,
    available_seats=5,
    current_trip=False
)

IDLE_DRIVER_2 = Driver(
    unique_id=randint(1000, 9999),
    current_location=(7.0491888, 125.5893258),
    is_online=True,
    available_seats=5,
    current_trip=False
)

DRIVERS.append(MATCHING_DRIVER)
DRIVERS.append(MISMATCHING_DRIVER_1)
DRIVERS.append(MISMATCHING_DRIVER_2)
DRIVERS.append(IDLE_DRIVER_1)
DRIVERS.append(IDLE_DRIVER_2)


##### Display Drivers #####
print("\nDRIVERS")
print("--------------------------")
for driver in DRIVERS:
    print("ID: {}; Location: {}; Seats Available: {}; Online: {}".format(
        driver.unique_id,
        driver.current_location,
        driver.available_seats,
        driver.is_online
    ))
print("\n")
##### TEST MODULE #####

print("TRIP TO MATCH DETAILS")
print("--------------------------")
print("Pickup: {}; DropOff: {}; Seats Reserved: {}".format(
    TRIP_TO_MATCH_1.start_node,
    TRIP_TO_MATCH_1.end_node,
    TRIP_TO_MATCH_1.seats_reserved
))

FARE_TO_PAY_1 = TRIP_TO_MATCH_1.get_fare()
print("Fare to Pay: ${}".format(FARE_TO_PAY_1))

## GET AVAILABLE DRIVERS FOR TRIP_TO_MATCH_1 ##
AVAILABLE_DRIVERS = TRIP_TO_MATCH_1.get_available_drivers(DRIVERS)

print("\nAvailable Drivers: ")
for driver in AVAILABLE_DRIVERS:
    distance = round(driver.get_distance(
        TRIP_TO_MATCH_1.start_node[0],
        TRIP_TO_MATCH_1.start_node[1]
    ), 2)
    print("ID: {}; Location: {}; Distance: {}; Seats Available: {}; Current Trip: {} TO {}".format(
        driver.unique_id,
        driver.current_location,
        "{}km".format(distance),
        driver.available_seats,
        driver.current_trip.start_node,
        driver.current_trip.end_node
    ))


## SELECT FROM THE LIST OF AVAILABLE DRIVERS THRU QUEUING ##
QUEUE_TIME = TRIP_CONFIG.process_time  # seconds
QUEUE_END = time.time() + QUEUE_TIME
driver_found = False
for driver in AVAILABLE_DRIVERS:
    if time.time() <= QUEUE_END:
        print("Accept Request? Y/N")
        response = input()
        if response.upper() == "Y":
            driver_found = True
            TRIP_TO_MATCH_1.driver = driver
            break
    else:
        break

if not driver_found and time.time() <= QUEUE_END:
    # IF NO DRIVER ACCEPTED THE RESPONSE,
    # INITIATE SEARCH FOR NEARBY IDLE DRIVERS
    ONLINE_DRIVERS = TRIP_TO_MATCH_1.get_online_drivers(DRIVERS)
    IDLE_DRIVERS = TRIP_TO_MATCH_1.get_idle_drivers(ONLINE_DRIVERS)
    print("\nSELECTING FROM IDLE DRIVERS:")
    for driver in IDLE_DRIVERS:
        print("Accept Request? Y/N")
        response = input()
        if response.upper() == "Y":
            driver_found = True
            TRIP_TO_MATCH_1.driver = driver
            break

if driver_found:
    print("\nFinal Assigned Driver:")

    distance = round(TRIP_TO_MATCH_1.driver.get_distance(
        TRIP_TO_MATCH_1.start_node[0],
        TRIP_TO_MATCH_1.start_node[1]
    ), 2)

    if TRIP_TO_MATCH_1.driver.current_trip:
        print("ID: {}; Location: {}; Distance: {}; Seats Available: {}; Current Trip: {} TO {}".format(
            TRIP_TO_MATCH_1.driver.unique_id,
            TRIP_TO_MATCH_1.driver.current_location,
            "{}km".format(distance),
            TRIP_TO_MATCH_1.driver.available_seats,
            TRIP_TO_MATCH_1.driver.current_trip.start_node,
            TRIP_TO_MATCH_1.driver.current_trip.end_node
        ))
    else:
        print("ID: {}; Location: {}; Distance: {}; Seats Available: {}; Trip: No Ongoing Trip".format(
            TRIP_TO_MATCH_1.driver.unique_id,
            TRIP_TO_MATCH_1.driver.current_location,
            "{}km".format(distance),
            TRIP_TO_MATCH_1.driver.available_seats,
        ))
else:
    print("No driver found for this trip.")


##### MISC FUNCTIONS #####

# Get the node value of a lat/long pair
# NODE_VALUE = TRIP_TO_MATCH_1.get_node(7.0649960, 125.6017195)
