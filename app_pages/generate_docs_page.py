import asyncio
import logging
import os
import shutil

import streamlit as st

from lib.common_icons import SERVER_ICON, TEST_ICON, DOCS_ICON, GENERATE_ICON, DOWNLOAD_ICON
from lib.mcpdoc_lib import MCPServerDoc
from lib.st_lib import set_current_page, show_info, show_error

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
LOG.info("Starting Manage Servers page")

set_current_page("generate_docs_page")

if not st.session_state.mcp_metadata.get("transport_type", ""):
    show_info("Please set the **Current MCP server** on the **Manage Servers** page.")
    LOG.info("No MCP server selected. Stopping further execution.")
    st.stop()

transport_type = st.session_state.mcp_metadata.get("transport_type", "")
server_name = st.session_state.mcp_metadata.get("name", "")
server_url = st.session_state.mcp_metadata.get("url", "")

st.subheader(f"{DOCS_ICON} Generate MCP Server Documentation [`{server_name}`]")

if st.button("Generate Documentation", type="primary", icon=GENERATE_ICON):
    with st.spinner("Generating documentation..."):
        try:
            mcpdoc = MCPServerDoc(server_name, transport_type, server_url)
            asyncio.run(mcpdoc.load_schema())
            report_folder = mcpdoc.generate_documentation()
            # get 2nd part of the report folder path
            report_folder_name = os.path.basename(report_folder)

            # Create a zip file of the report folder
            shutil.make_archive("reports/" + report_folder_name, 'zip', report_folder)

            with open("reports/" + report_folder_name + ".zip", "rb") as f:
                st.download_button(
                    label="Download Documentation",
                    data=f,
                    file_name=report_folder_name + ".zip",
                    mime="application/zip",
                    icon=DOWNLOAD_ICON
                )

        except Exception as e:
            show_error(f"Error generating documentation: {e}")
            LOG.error(f"Error generating documentation: {e}")