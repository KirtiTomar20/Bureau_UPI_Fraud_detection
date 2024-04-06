import numpy as np


def generate_lat_long(city_center_lat, city_center_long, num_points=10000, max_distance_km=10,min_distance=0):
    """
    Generate latitude and longitude points within a specified distance from a central point.

    :param city_center_lat: Latitude of the city center in radians.
    :param city_center_long: Longitude of the city center in radians.
    :param num_points: Number of points to generate.
    :param max_distance_km: Maximum distance from the center in kilometers.
    :param min_distance: Minimum distance from the center in kilometers.
    :return: List of (latitude, longitude) tuples in degrees.
    """
    # Earth's radius in kilometers
    R = 6378.1

    # Convert max_distance_km to radians
    max_distance_rad = max_distance_km / R

    # Generate random angles and distances
    angles = np.random.uniform(low=0, high=2 * np.pi, size=num_points)
    distances = np.random.uniform(low=min_distance, high=max_distance_rad, size=num_points)

    # Calculate latitudes and longitudes
    latitudes = np.arcsin(np.sin(city_center_lat) * np.cos(distances) +
                          np.cos(city_center_lat) * np.sin(distances) * np.cos(angles))
    longitudes = city_center_long + np.arctan2(np.sin(angles) * np.sin(distances) * np.cos(city_center_lat),
                                               np.cos(distances) - np.sin(city_center_lat) * np.sin(latitudes))

    # Convert radian latitudes and longitudes to degrees
    latitudes_deg = np.degrees(latitudes)
    longitudes_deg = np.degrees(longitudes)

    # Return list of tuples
    return list(zip(latitudes_deg, longitudes_deg))


# New York City's approximate center in radians for calculation
# nyc_center_lat = np.radians(40.7128)
# nyc_center_long = np.radians(-74.0060)
#
# # Generate 10 random latitude and longitude points within about 10km of NYC center
# generated_points = generate_lat_long(nyc_center_lat, nyc_center_long, num_points=1, max_distance_km=10)
#
# for point in generated_points:
#     print(point[1])
