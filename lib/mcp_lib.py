import logging
import streamlit as st
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

LOG = logging.getLogger(__name__)


async def display_capabilities(session):
    tool_list = []
    tool_result = await session.list_tools()

    for tool in tool_result.tools:
        tool_list.append(
            {
                "Name": tool.name,
                "Description": tool.description,
                "InputSchema": tool.inputSchema,
                "Model_json": tool.model_dump_json(),
            }
        )
    LOG.info(f"Tool list: {tool_list}")
    st.session_state.mcp_metadata["tools"] = tool_list

    # try:
    #     # Get resources
    #     resource_list = []
    #     resource_result = await session.list_resources()
    #
    #     for resource in resource_result.resources:
    #         resource_list.append(
    #             {
    #                 "Name": resource.name,
    #                 "Description": resource.description,
    #                 # "InputSchema": resource.,
    #                 "Model_json": resource.model_dump_json(),
    #             }
    #         )
    # except Exception as e:
    #     st.error(f"Unable to fetch resources: {e}")


async def populate_sse_mcp_server_capabilities(mcp_server_url):
    """
    Fetch the capabilities of the MCP server using SSE.
    """

    async with sse_client(mcp_server_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()
            # Get tools
            await display_capabilities(session)


async def get_stdio_mcp_server_capabilities(mcp_command: str, mcp_arguments: list):
    """
    Fetch the capabilities of the MCP server using STDIO.
    """

    server_params = StdioServerParameters(
        command=mcp_command,
        args=mcp_arguments,
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Get tools
            await display_capabilities(session)