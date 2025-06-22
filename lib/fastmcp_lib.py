from fastmcp import Client
import asyncio
import streamlit as st

async def get_client() -> Client:
    """
    Get a FastMCP client for making requests.
    :return: FastMCP client
    """
    client = None
    if st.session_state.mcp_metadata['transport_type'] == 'SSE':
        client =  Client(st.session_state.mcp_metadata['url'])
    elif st.session_state.mcp_metadata['transport_type'] == 'STDIO':
        st.error("STDIO transport is not supported at present.")
        client = None
    return client


async def get_tools(client: Client) -> list:
    """
    Get the list of tools from the MCP server.
    :param client: FastMCP client
    :return: List of tools
    """
    if not client:
        st.error("Client is not initialized.")
        return []

    try:
        async with client:
            tools = await client.list_tools()
            return tools
    except Exception as e:
        # st.error(f"Error fetching tools: {e}")
        return []



async def test_selected_server(transport_type: str, url: str):
    """
    Test the selected MCP server by checking if it is reachable.
    :param transport_type: Transport type of the MCP server
    :param url: URL of the MCP server
    """

    try:
        client = await get_client()
        async with client:
            tools = await get_tools(client)
            if not tools:
                raise Exception("Cannot fetch tools from the MCP server. Please check the server URL or transport type.")
    except Exception as e:
        raise Exception(f"{e}!")
