
from langchain_core.tools import tool


@tool
def calculate_fertilizer(
    land_area_acres: float,
    fertilizer_per_acre: float
) -> str:
    """
    Calculate the total fertilizer required.

    Args:
        land_area_acres: Total land area in acres.
        fertilizer_per_acre: Fertilizer amount in kg per acre.
    """

    if land_area_acres <= 0 or fertilizer_per_acre < 0:
        return "Please provide valid land and fertilizer values."

    total = land_area_acres * fertilizer_per_acre

    return f"Total fertilizer required: {total:.2f} kg"
