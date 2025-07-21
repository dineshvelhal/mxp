import json
import logging

from fastmcp import Client
import streamlit as st
from fastmcp.client import SSETransport, StreamableHttpTransport

LOG = logging.getLogger(__name__)


async def get_client() -> Client:
    """
    Get a FastMCP client for making requests.
    :return: FastMCP client
    """
    client = None
    if st.session_state.mcp_metadata['transport_type'] == 'SSE':
        transport = SSETransport(url=st.session_state.mcp_metadata['url'])
        client = Client(transport=transport)
    elif st.session_state.mcp_metadata['transport_type'] == 'Streamable-HTTP':
        transport = StreamableHttpTransport(url=st.session_state.mcp_metadata['url'])
        client = Client(transport=transport)

    return client


async def get_tools() -> (list, str):
    """
    Get the list of tools from the MCP server.
    :return: List of tools
    """

    tool_list = []

    client = await get_client()

    try:
        async with client:
            tools = await client.list_tools()
            for tool in tools:
                tool_row = {
                    "NAME": tool.name,
                    "TITLE": tool.title,
                    "DESCRIPTION": tool.description,
                    "MODEL_JSON": tool.model_dump_json(),
                    "INPUT_SCHEMA": tool.inputSchema
                }
                tool_list.append(tool_row)

    except Exception as e:
        # st.error(f"Error fetching tools: {e}")
        return [], f"{e}"

    if len(tool_list) == 0:
        return [], "No tools found on the MCP server."

    return tool_list, "Success"


async def test_selected_server(transport_type: str, url: str):
    """
    Test the selected MCP server by checking if it is reachable.
    :param transport_type: Transport type of the MCP server
    :param url: URL of the MCP server
    """
    try:
        client = None
        if transport_type == 'SSE':
            transport = SSETransport(url)
            client = Client(transport=transport)
        elif transport_type == 'Streamable-HTTP':
            transport = StreamableHttpTransport(url)
            client = Client(transport=transport)
        else:
            raise ValueError(f"Unsupported transport type: {transport_type}")

        async with client:
            pass
            # tools = await client.list_tools()
            # if not tools:
            #     raise Exception("Cannot fetch tools from the MCP server. Please check the server URL or transport type.")
        return True, "Server is reachable"
    except Exception as e:
        return False, f"{e}"



async def call_tool(tool_call: dict):
    """
    Call a tool on the MCP server.
    :param tool_call: Tool call dictionary containing tool name and arguments
    :return: Tool response
    """
    client = await get_client()

    try:
        async with client:
            response = await client.call_tool(tool_call.function.name, json.loads(tool_call.function.arguments))
            return response, "Success"
    except Exception as e:
        LOG.error(f"Error calling tool: {e}")
        return None, f"Error calling tool: {e}"
