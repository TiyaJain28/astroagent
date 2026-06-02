from geopy.geocoders import Nominatim


def geocode_place(place: str):
    geolocator = Nominatim(user_agent="astroagent")

    location = geolocator.geocode(place)

    if not location:
        return {
            "success": False,
            "error": "Place not found"
        }

    return {
        "success": True,
        "place": place,
        "latitude": location.latitude,
        "longitude": location.longitude
    }