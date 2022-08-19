
# import module
import json
from geopy.geocoders import Nominatim

# initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")

def lambda_handler(myevent, _):
    # Latitude & Longitude input
    Latitude = myevent["lat"]
    Longitude = myevent["long"]

    location = geolocator.reverse(Latitude+","+Longitude)

    address = location.raw['address']

    # traverse the data
    return {
        "statusCode": 200,
        "body": json.dumps(address),
        "headers": {
            "Content-Type": "application/json",
        }
    }