import json
import math
import time
import googlemaps
import pyperclip
import os

from dotenv import load_dotenv

load_dotenv()


def create_circle_coordinates(lat, lng, radius, num_points=36):
    """
    Generates coordinates approximating a circle on the Earth's surface.

    :param lat: Latitude of the center point.
    :param lng: Longitude of the center point.
    :param radius: Radius in meters.
    :param num_points: Number of points to generate.
    :return: A list of [lng, lat] coordinates.
    """
    # Earth's radius in meters
    earth_radius = 6378137

    # Array to hold the points
    coordinates = []

    # Calculate angular distance covered on earth's surface
    angular_distance = radius / earth_radius

    for i in range(num_points):
        # Calculate angle
        theta = (i * (360 / num_points)) * (math.pi / 180)

        # Calculate point's lat and lng
        point_lat = math.asin(
            math.sin(lat * (math.pi / 180)) * math.cos(angular_distance)
            + math.cos(lat * (math.pi / 180))
            * math.sin(angular_distance)
            * math.cos(theta)
        )
        point_lng = lng * (math.pi / 180) + math.atan2(
            math.sin(theta)
            * math.sin(angular_distance)
            * math.cos(lat * (math.pi / 180)),
            math.cos(angular_distance)
            - math.sin(lat * (math.pi / 180)) * math.sin(point_lat),
        )

        # Convert back to degrees
        point_lat = point_lat * (180 / math.pi)
        point_lng = point_lng * (180 / math.pi)

        # Append this point to our coordinates array
        coordinates.append([point_lng, point_lat])

    # Ensure the polygon is closed by adding the starting point at the end.
    coordinates.append(coordinates[0])

    return coordinates


def get_all_places(client, initial_places_result):
    """
    Collects all places from the initial result and subsequent pages.

    :param client: The Google Maps client instance.
    :param initial_places_result: The initial result object from a Places API nearby search.
    :return: A list of all places from all pages.
    """
    places = initial_places_result["results"]
    while "next_page_token" in initial_places_result:
        print("Fetching next page...")
        time.sleep(2)  # Ensure the next page token is valid before using it
        next_page_token = initial_places_result["next_page_token"]
        next_places_result = client.places_nearby(page_token=next_page_token)
        places.extend(next_places_result["results"])
        initial_places_result = next_places_result
    return places


def get_places_for_keywords(client, location, radius, keywords):
    all_places = []
    for keyword in keywords:
        initial_places_result = client.places_nearby(
            location=location, radius=radius, keyword=keyword
        )
        places = get_all_places(client, initial_places_result)
        all_places.extend(places)

    # Deduplicate places based on place_id
    unique_places = {place["place_id"]: place for place in all_places}.values()

    return list(unique_places)


def boba_tea_shops_geojson(api_key, latitude, longitude, radius, keywords):
    # Initialize the client with your API key
    gmaps = googlemaps.Client(key=api_key)
    location = (latitude, longitude)

    # Handle pagination to get all places
    all_places = get_places_for_keywords(gmaps, location, radius, keywords)

    # Prepare the GeoJSON structure
    geojson = {"type": "FeatureCollection", "features": []}

    # Add the search area as a circle (approximated by a polygon)
    circle_coordinates = create_circle_coordinates(latitude, longitude, radius)
    geojson["features"].append(
        {
            "type": "Feature",
            "geometry": {"type": "Polygon", "coordinates": [circle_coordinates]},
            "properties": {"name": "Search Area", "radius": radius},
        }
    )

    # Counter for unique IDs
    place_id_counter = 1

    for place in all_places:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    place["geometry"]["location"]["lng"],
                    place["geometry"]["location"]["lat"],
                ],
            },
            "properties": {
                "id": place_id_counter,  # Assign the current counter value as the ID
                "name": place.get("name"),
                "address": place.get("vicinity"),
            },
        }
        geojson["features"].append(feature)
        place_id_counter += 1  # Increment the counter for the next place

    # Define static points to add to every response
    static_points = [
        {
            "type": "Feature",
            "properties": {
                "marker-color": "#1c5932",
                "marker-size": "medium",
                "marker-symbol": "cafe",
                "name": "Timekeeper's Haus",
            },
            "geometry": {
                "coordinates": [-97.23504427657171, 33.13097255140205],
                "type": "Point",
            },
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-97.28144581829838, 33.02564523168062],
            },
            "properties": {
                "name": "Champ Donut Company",
                "address": "3556 TX-114 #402, Fort Worth, TX 76177",
            },
        },
        {
            "type": "Feature",
            "properties": {
                "stroke": "#555555",
                "stroke-width": 2,
                "stroke-opacity": 1,
                "fill": "#fb0404",
                "fill-opacity": 0.5,
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-97.23371531116045, 33.241179481034166],
                        [-97.24681463221584, 33.240640564032944],
                        [-97.25978731971753, 33.23902902291537],
                        [-97.27250797822776, 33.23636043639754],
                        [-97.2848536758929, 33.23266059971977],
                        [-97.29670514476663, 33.227965272533055],
                        [-97.30794794378936, 33.22231982955001],
                        [-97.31847357266619, 33.21577881751882],
                        [-97.3281805254625, 33.20840542302263],
                        [-97.33697527343702, 33.20027085649813],
                        [-97.34477316744874, 33.191453658695735],
                        [-97.35149925118841, 33.1820389365612],
                        [-97.35708897748837, 33.17211753619674],
                        [-97.36148882103544, 33.161785161152494],
                        [-97.36465678193954, 33.15114144480168],
                        [-97.36656277577615, 33.140288985960495],
                        [-97.36718890691039, 33.129332357224925],
                        [-97.36652962310762, 33.11837709570959],
                        [-97.3645917506279, 33.10752868598838],
                        [-97.36139441017345, 33.09689154505402],
                        [-97.356968815201, 33.08656801903634],
                        [-97.3513579552109, 33.07665740124919],
                        [-97.3446161676748, 33.06725498087812],
                        [-97.3368086032558, 33.05845113127866],
                        [-97.32801058990256, 33.05033044643476],
                        [-97.31830690225581, 33.04297093363239],
                        [-97.30779094359197, 33.03644326984178],
                        [-97.29656384823588, 33.03081012867853],
                        [-97.2847335130067, 33.026125584135585],
                        [-97.27241356681252, 33.02243459655083],
                        [-97.25972228798247, 33.01977258550578],
                        [-97.24678147931814, 33.018165093545825],
                        [-97.23371531116045, 33.017627543778076],
                        [-97.22064914300275, 33.018165093545825],
                        [-97.20770833433843, 33.01977258550578],
                        [-97.19501705550839, 33.02243459655083],
                        [-97.1826971093142, 33.026125584135585],
                        [-97.17086677408501, 33.03081012867853],
                        [-97.15963967872894, 33.03644326984178],
                        [-97.14912372006508, 33.04297093363239],
                        [-97.13942003241833, 33.05033044643476],
                        [-97.13062201906509, 33.05845113127866],
                        [-97.1228144546461, 33.06725498087812],
                        [-97.11607266710999, 33.07665740124919],
                        [-97.11046180711989, 33.08656801903634],
                        [-97.10603621214744, 33.09689154505402],
                        [-97.102838871693, 33.10752868598838],
                        [-97.10090099921327, 33.11837709570959],
                        [-97.10024171541052, 33.129332357224925],
                        [-97.10086784654474, 33.140288985960495],
                        [-97.10277384038136, 33.15114144480168],
                        [-97.10594180128545, 33.161785161152494],
                        [-97.11034164483252, 33.17211753619674],
                        [-97.11593137113249, 33.1820389365612],
                        [-97.12265745487215, 33.191453658695735],
                        [-97.13045534888388, 33.20027085649813],
                        [-97.13925009685842, 33.20840542302263],
                        [-97.1489570496547, 33.21577881751882],
                        [-97.15948267853155, 33.22231982955001],
                        [-97.17072547755426, 33.227965272533055],
                        [-97.18257694642799, 33.23266059971977],
                        [-97.19492264409314, 33.23636043639754],
                        [-97.20764330260336, 33.23902902291537],
                        [-97.22061599010506, 33.240640564032944],
                        [-97.23371531116045, 33.241179481034166],
                    ]
                ],
            },
        },
    ]

    for point in static_points:
        point["properties"]["id"] = place_id_counter
        geojson["features"].append(point)
        place_id_counter += 1  # Ensure each static point also gets a unique ID

    # Return the GeoJSON object
    return geojson


# Example usage
api_key = os.getenv("API_KEY")
latitude = 32.96177363984826
longitude = -97.11511862649252
radius = 40000  # meters

# 33.101729782995356, -97.23372386848219
keywords = [
    "boba",
    "bubble tea",
    "boba tea",
    "milk tea",
    "tapioca tea",
    "boba shop",
    "bubble tea shop",
    "milk tea shop",
]
geojson_output = boba_tea_shops_geojson(api_key, latitude, longitude, radius, keywords)
geojson_str = json.dumps(geojson_output, indent=2)  # Pretty print the GeoJSON

# Print the GeoJSON string
# print(geojson_str)
print("Found {} places".format(len(geojson_output["features"])))

# Copy the GeoJSON string to the clipboard
pyperclip.copy(geojson_str)

print("GeoJSON output has been copied to the clipboard.")
