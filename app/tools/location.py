import requests


def get_location_coordinates(location: str):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": location,
        "count": 5,
        "language": "en",
        "countryCode": "LK"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return None

        place = results[0]

        return {
            "name": place["name"],
            "country": place.get("country", ""),
            "latitude": place["latitude"],
            "longitude": place["longitude"]
        }

    except requests.RequestException as error:
        print(f"Geocoding API error: {error}")
        return None