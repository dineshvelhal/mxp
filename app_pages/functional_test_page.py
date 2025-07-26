import logging
import os
import streamlit as st

from lib.common_icons import TEST_ICON, SERVER_ICON
from lib.st_lib import set_current_page, show_info

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
LOG.info("Starting Manage Servers page")

set_current_page("functional_test_page")

if not st.session_state.mcp_metadata.get("transport_type", ""):
    show_info("Please set the **Current MCP server** on the **Manage Servers** page.")
    LOG.info("No MCP server selected. Stopping further execution.")
    st.stop()

transport_type = st.session_state.mcp_metadata.get("transport_type", "")
server_name = st.session_state.mcp_metadata.get("name", "")
server_url = st.session_state.mcp_metadata.get("url", "")

st.subheader(f"{TEST_ICON} Functional Testing [Server Name: `{server_name}`]")