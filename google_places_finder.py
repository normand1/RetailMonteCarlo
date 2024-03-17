import googlemaps
import requests


class GooglePlacesFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = googlemaps.Client(key=api_key)
        self.base_url = "https://maps.googleapis.com/maps/api/place/details/json"

    def find_coffee_shops(self, location, radius=1000):
        places_result = self.client.places_nearby(
            location=location, radius=radius, type="cafe"
        )
        results = places_result.get("results", [])
        return [results[0]] if results else None

    def get_place_details(self, place_id, fields="website"):
        params = {"place_id": place_id, "fields": fields, "key": self.api_key}
        response = requests.get(self.base_url, params=params)
        details = response.json()
        return details.get("result", {})
