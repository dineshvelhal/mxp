import asyncio
import logging
import pandas as pd
import streamlit as st

from lib.mcp_lib import get_sse_mcp_server_capabilities

LOG = logging.getLogger(__name__)
LOG.info("Starting MCP Explore page")

st.subheader("Explore MCP Servers")
col1, col2 = st.columns(2)

with col1:
    transport_type = st.selectbox("Select Transport Type",
                                  options=["STDIO", "SSE"],
                                  format_func=lambda x: "STDIO (Standard Input & Output)" if x == "STDIO" else "SSE (Server-Sent Events)",
                                  index=0,
                                  help="Transport type is how client communicates with the server. ")
    st.session_state.mcp_transport_type = transport_type

with col2:
    if transport_type == "STDIO":
        LOG.info("Selected transport type: STDIO")
        command = st.selectbox("Select Command",
                               options=["python", "uvx", "npx", "docker"],
                               help="When STDIO transport type is selected, the MCP server runs as a local process. "
                               "You need to specify the command that invokes the MCP server. ")
        st.session_state.mcp_command = command
        LOG.info(f"Selected MCP command: {command}")

        arguments = pd.DataFrame([], columns=["Arguments"])
        arguments_editor = st.data_editor(arguments,
                                          use_container_width=True,
                                          hide_index=True,
                                          num_rows="dynamic")

        for arg in arguments_editor["Arguments"].tolist():
            if arg:
                pass
            else:
                st.stop()

        # Check if the user has provided arguments
        if not arguments_editor.empty:
            st.session_state.mcp_arguments = arguments_editor["Arguments"].tolist()
            LOG.info(f"Selected MCP arguments: {st.session_state.mcp_arguments}")
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

            st.session_state.mcp_sse_url = sse_url
            LOG.info(f"Selected MCP SSE URL: {sse_url}")
        else:
            st.session_state.mcp_sse_url = None
            LOG.info("No MCP SSE URL provided.")
            st.stop()
    else:
        st.error("Invalid transport type selected. Please select either STDIO or SSE.")
        st.stop()

if st.button("Load MCP Details",
             key="load_mcp_details",
             help="Click to load MCP supported tools",
             type="primary"):

    tool_list = asyncio.run(get_sse_mcp_server_capabilities(st.session_state.mcp_sse_url))

    if tool_list:
        st.write("**MCP Server Capabilities**")
        st.dataframe(tool_list,)