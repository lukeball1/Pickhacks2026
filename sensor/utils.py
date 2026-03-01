import math
import random
import requests


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Returns distance in meters between two GPS points
    """
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_current_location():
    """
    Placeholder: get vehicle GPS
    Returns dict with lat/lng
    """
    response = requests.get("http://localhost:5000/gps")
    return response.json()
