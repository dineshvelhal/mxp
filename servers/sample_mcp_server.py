from fastmcp import FastMCP

mcp = FastMCP(name="Sample MCP Server",)

# Define a Tool
@mcp.tool()
def greet_user(name: str) -> str:
    """Greets a user by name."""
    return f"Hello, {name}!"

# Define a Resource
@mcp.resource(uri="info://about_server",
              description="Information about the MCP server",)
def get_main_server_info() -> str:
    """Provides information about this MCP server."""
    return "This is a sample MCP server demonstrating tools, resources, and prompts."


# Define a Resource
@mcp.resource(uri="info://{server_name}/about_server",
              description="Information about the MCP server",)
def get_given_server_info(server_name: str) -> str:
    """Provides information about this MCP server."""
    return f"This is a sample MCP server ({server_name})demonstrating tools, resources, and prompts."


# Define a Prompt
@mcp.prompt(description="Summarizes a given text.")
def summarize_text_prompt(text: str) -> str:
    """
    Generate a prompt to summarize the provided text.
    Args:
        text (str): The text to be summarized.
    Returns:
        str: The generated prompt.
    """
    return f"Please provide a concise summary of the following text:\n\n{text}"


@mcp.prompt(description="list of all US states")
def list_of_states_prompt() -> str:
    """
    Generate a prompt to summarize the provided text.
    Args:
        text (str): The text to be summarized.
    Returns:
        str: The generated prompt.
    """
    return f"Please provide a list of all US states in alphabetical order."

if __name__ == "__main__":
    # Run the MCP server
    mcp.run(transport="sse", port=8050)