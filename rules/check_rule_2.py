import math
from datetime import datetime, timedelta


def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the distance between two points on the Earth.
    radius = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance


def verify(transactions):
    # Assuming `transactions` is a list of transaction dictionaries for a specific card
    # Each transaction dictionary must have `amount`, `latitude`, `longitude`, and `dateTimeTransaction` keys

    total_amount = 0
    unique_locations = []

    # Filter transactions in the last 12 hours

    for transaction in transactions:
        total_amount += float(transaction['transactionAmount'])
        is_unique_location = True

        for location in unique_locations:
            if calculate_distance(float(transaction['latitude']), float(transaction['longitude']), location[0],
                                  location[1]) < 200:
                is_unique_location = False
                break

        if is_unique_location:
            unique_locations.append((float(transaction['latitude']), float(transaction['longitude'])))

    # Checking the rule condition
    if total_amount >= 100000 and len(unique_locations) > 5:
        return 1
    else:
        return 0

