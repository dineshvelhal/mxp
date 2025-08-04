from typing import Annotated

from mcp.server import FastMCP
from pydantic import Field

mcp = FastMCP(name="BMI MCP Server",
              host="0.0.0.0",
              port=8050)

@mcp.tool(annotations={"idempotentHint": True}, description="Returns the Body Mass Index (BMI) based on the provided weight (Kg) and height (meters).")
def calculate_bmi(weight: Annotated[float, Field(description="Weight in kilograms")],
                  height: Annotated[float, Field(description="Height in meters")]) -> float:
    """
    Returns the Body Mass Index (BMI) based on the provided weight (Kg) and height (meters).

    :param weight: weight in kilograms
    :param height: height in meters
    :return: BMI (Body Mass Index) calculated as weight divided by the square of height.
    """
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight <= 0:
        raise ValueError("Weight must be greater than zero.")
    if weight > 500:
        raise ValueError("Weight exceeds the maximum limit of 500 kg.")
    if height > 3:
        raise ValueError("Height exceeds the maximum limit of 3 meters.")

    return weight / (height ** 2)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="sse")