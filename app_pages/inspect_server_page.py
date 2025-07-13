import asyncio
import logging
import pandas as pd
import streamlit as st

from lib.fastmcp_lib import get_tools, get_client
# from lib.mcp_lib import populate_sse_mcp_server_capabilities, populate_stdio_mcp_server_capabilities
from lib.st_lib import display_mcp_summary, set_current_page, show_info

LOG = logging.getLogger(__name__)
LOG.info("Starting MCP Explore page")

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

set_current_page("mcp_explore_page")

st.subheader(":material/troubleshoot: Inspect MCP Server capabilities")

if not st.session_state.mcp_metadata.get("transport_type", ""):
    show_info("Please set the **Current MCP server** on the **Manage Servers** page.")
    LOG.info("No MCP server selected. Stopping further execution.")
    st.stop()

transport_type = st.session_state.mcp_metadata.get("transport_type", "")
if transport_type == "SSE":
    sse_url = st.session_state.mcp_metadata.get("url", "")
elif transport_type == "Streamable-HTTP":
    s_http_url = st.session_state.mcp_metadata.get("url", "")

if st.button(f"Load Server [{st.session_state.mcp_metadata['name']}]",
             key="load_mcp_details",
             help="Click to load MCP supported tools",
             type="primary"):
    LOG.info("Load MCP server details button clicked")
    with st.spinner("Loading MCP server details...", show_time=True):
        # mcp_client = asyncio.run(get_client())
        mcp_tools = asyncio.run(get_tools())

        display_mcp_summary()
