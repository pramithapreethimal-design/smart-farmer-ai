farmer_profiles = {
    "farmer_001": {
        "name": "Kamal",
        "location": "Kurunegala",
        "main_crop": "Rice",
        "land_area": 2.5
    },
    "farmer_002": {
        "name": "Nimal",
        "location": "Anuradhapura",
        "main_crop": "Chili",
        "land_area": 1.5
    }
}


def get_farmer_profile(farmer_id):

    return farmer_profiles.get(farmer_id)