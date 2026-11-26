
import requests

from langchain_core.tools import tool
from app.tools.location import get_location_coordinates


@tool
def get_weather_by_location(location: str) -> str:
    """
    Get current weather using a city or location name.

    Args:
        location: Name of the location in Sri Lanka.
    """

    # Step 1: Get coordinates
    coordinates = get_location_coordinates(location)

    if not coordinates:
        return f"Could not find location: {location}"

    latitude = coordinates["latitude"]
    longitude = coordinates["longitude"]

    # Step 2: Request weather data
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m"
        ],
        "timezone": "auto"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()
        current = data["current"]

        return (
            f"Weather for {coordinates['name']}, "
            f"{coordinates['country']}\n"
            f"Temperature: {current['temperature_2m']} °C\n"
            f"Humidity: {current['relative_humidity_2m']}%\n"
            f"Precipitation: {current['precipitation']} mm\n"
            f"Wind Speed: {current['wind_speed_10m']} km/h"
        )

    except requests.RequestException as error:
        return f"Weather API error: {error}"

    except (KeyError, TypeError):
        return "Could not process weather information."
