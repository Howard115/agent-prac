from pydantic_settings import BaseSettings
import requests

class GoogleAPISettings(BaseSettings):
    """Settings for Google Places API"""
    GOOGLE_MAPS_API_KEY: str = None
    default_location: str = "25.0338,121.5646"
    default_radius: int = 5000
    default_language: str = "zh-TW"
    default_keyword: str = "牛排"


def get_nearby_restaurants(
    location: str | None = None,
    radius: int | None = None
):
    """
    Fetches nearby restaurants using the Google Places API.

    Args:
        settings (GoogleAPISettings): Pydantic settings object containing API configuration
        location (str, optional): The latitude/longitude coordinates. Defaults to settings value.
        radius (int, optional): The radius (in meters) within which to search. Defaults to settings value.

    Returns:
        list: A list of dictionaries containing restaurant information
    """
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        f"?location={location or settings.default_location}"
        f"&radius={radius or settings.default_radius}"
        f"&keyword={settings.default_keyword}"
        f"&language={settings.default_language}"
        f"&key={settings.GOOGLE_MAPS_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        if data['status'] == 'OK':
            return data['results']
        else:
            print(f"Error: {data['status']}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return []

# Example usage:
settings = GoogleAPISettings()  # Will load from environment variables
restaurants = get_nearby_restaurants()

for restaurant in restaurants:
    print(f"Restaurant: {restaurant['name']}")
    print(f"Address: {restaurant['vicinity']}")
    print(f"Rating: {restaurant['rating']}")
    # ... extract and print other desired information
    
