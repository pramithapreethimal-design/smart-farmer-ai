from langchain_core.tools import tool


@tool
def get_crop_information(crop_name: str) -> str:
    """
    Get basic growing information about a crop.

    Args:
        crop_name: Name of the crop.
    """

    crop_data = {
        "rice": (
            "Rice needs suitable water management, "
            "sunlight and proper nutrient management."
        ),

        "tomato": (
            "Tomato needs well-drained soil, "
            "sunlight and regular watering."
        ),

        "chili": (
            "Chili needs sunlight, well-drained soil "
            "and careful watering."
        )
    }

    crop = crop_name.lower().strip()

    if crop in crop_data:
        return crop_data[crop]

    return f"No crop information available for {crop_name}."