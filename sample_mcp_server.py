from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Weather Service",
              host="0.0.0.0",
              port=8050)


@mcp.tool()
def get_weather(location: str = "Dallas") -> str:
    """Get the current weather for a specified location."""
    return f"Weather in {location}: Sunny, 72°F"


@mcp.tool(annotations={
        "title": "Calculate BMI",
    "readOnlyHint": True
    })
def get_bmi(weight: float, height: float) -> float:
    """Calculate the Body Mass Index (BMI) given weight and height.

It accepts following parameters:
weight: Person's weight in kilograms
height: Person's height in meters

It returns:
:return: Body Mass Index (BMI)
    """
    if height <= 0:
        raise ValueError("Height must be greater than zero.")
    return weight / (height ** 2)


@mcp.resource(uri="file://{file_path}", mime_type="text/plain")
def file_resource(file_path: str) -> str:
    """Read the contents of a file at the specified path."""
    with open(file_path, 'r') as f:
        return f.read()


if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="sse")