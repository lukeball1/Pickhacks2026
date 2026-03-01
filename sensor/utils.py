import requests

def get_current_location():
    """
    Placeholder: get vehicle GPS
    Returns dict with lat/lng
    """
    response = requests.get("http://localhost:5000/gps")
    return response.json()
