import logging
import streamlit as st
from mcp import ClientSession
from mcp.client.sse import sse_client

LOG = logging.getLogger(__name__)

async def populate_sse_mcp_server_capabilities(mcp_server_url):
    """
    Fetch the capabilities of the MCP server using SSE.
    """

    async with sse_client(mcp_server_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Get tools
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


async def get_stdio_mcp_server_capabilities(mcp_server_command, mcp_server_args):
    """
    Fetch the capabilities of the MCP server using STDIO.
    """
    pass