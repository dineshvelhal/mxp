import asyncio
import logging
import pandas as pd
import streamlit as st

from lib.mcp_lib import populate_sse_mcp_server_capabilities, get_stdio_mcp_server_capabilities
from lib.st_lib import display_mcp_summary, set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting MCP Explore page")

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

set_current_page("mcp_explore_page")


st.subheader("🔍 Explore MCP Servers")
col1, col2 = st.columns(2)

with col1:
    transport_type = st.selectbox("Select Transport Type",
                                  options=["STDIO", "SSE"],
                                  format_func=lambda x: "STDIO (Standard Input & Output)" if x == "STDIO" else "SSE (Server-Sent Events)",
                                  index=0,
                                  help="Transport type is how client communicates with the server. ")

    LOG.info(f"Transport Type: {transport_type}")

with col2:
    if transport_type == "STDIO":
        LOG.info("Selected transport type: STDIO")
        command = st.selectbox("Select Command",
                               options=["npx", "docker", "python", "uvx"],
                               help="When STDIO transport type is selected, the MCP server runs as a local process. "
                               "You need to specify the command that invokes the MCP server. ")

        LOG.info(f"Selected MCP command: {command}")

        arguments = pd.DataFrame([], columns=["Arguments"])
        arguments_editor = st.data_editor(arguments,
                                          use_container_width=True,
                                          num_rows="dynamic")

        for arg in arguments_editor["Arguments"].tolist():
            if arg:
                pass
            else:
                st.stop()

        # Check if the user has provided arguments
        if not arguments_editor.empty:
            st.session_state.mcp_metadata["command_args"] = arguments_editor["Arguments"].tolist()
            LOG.info(f"Selected MCP arguments: {arguments_editor["Arguments"].tolist()}")
        else:
            st.session_state.mcp_arguments = []
            LOG.info("No MCP arguments provided.")
            st.stop()

    elif transport_type == "SSE":
        sse_url = st.text_input("Enter SSE URL",
                                placeholder="https://example.com/sse",
                                help="When SSE transport type is selected, the MCP server runs as a remote process. "
                                "You need to specify the URL of the MCP server.")

        if sse_url:
            # Check if the URL is valid
            if not sse_url.startswith("http://") and not sse_url.startswith("https://"):
                st.error("Invalid URL format. Please enter a valid URL starting with http:// or https://.")
                st.stop()

            st.session_state.mcp_metadata["url"] = sse_url
            LOG.info(f"Selected MCP SSE URL: {st.session_state.mcp_metadata["url"]}")
        else:
            st.session_state.mcp_sse_url = None
            LOG.info("No MCP SSE URL provided.")
            st.stop()
    else:
        st.error("Invalid transport type selected. Please select either STDIO or SSE.")
        st.stop()



if st.button("Load Server Details",
             key="load_mcp_details",
             help="Click to load MCP supported tools",
             type="primary"):

    st.session_state.mcp_metadata["transport_type"] = transport_type
    if transport_type == "STDIO":
        st.session_state.mcp_metadata["command"] = command
        st.session_state.mcp_metadata["command_args"] = arguments_editor["Arguments"].tolist()
        asyncio.run(get_stdio_mcp_server_capabilities(command, arguments_editor["Arguments"].tolist()))
    elif transport_type == "SSE":
        st.session_state.mcp_metadata["url"] = sse_url
        asyncio.run(populate_sse_mcp_server_capabilities(sse_url))

    display_mcp_summary()
