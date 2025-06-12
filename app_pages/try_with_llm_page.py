import asyncio
import logging

import pandas as pd
import streamlit as st

from lib.fastmcp_lib import get_client, get_tools
from lib.st_lib import set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting High Level Evaluation page")

st.subheader("🤝 Try MCP Server with LLM")

set_current_page("try_with_llm_page")

if not st.session_state.mcp_metadata['transport_type']:
    st.info("ℹ️ Please load the MCP server details on the MCP Explorer page")
    st.stop()

col1, col2 = st.columns([3, 1], vertical_alignment="center")
with col1:
    user_question = st.text_area("Question to LLM",
                                 height=100,
                                 placeholder="Ask your question",
                                 label_visibility="collapsed",)
with col2:
    go_button_clicked = st.button("Go", type="primary")

if go_button_clicked:
    if not user_question:
        st.error("Please enter a question to ask the LLM")
    else:
        with st.status("Plugged in MCP Server"):
            st.write(f"Transport: {st.session_state.mcp_metadata['transport_type']}")
            st.write(f"Server URL: {st.session_state.mcp_metadata['url']}")
            st.write(f"Command: {st.session_state.mcp_metadata['command']}")
            st.write(f"Arguments: {st.session_state.mcp_metadata['command_args']}")

        with st.status("Fetching tools from MCP server"):
            # Get the client and tools
            client = asyncio.run(get_client())
            tools = asyncio.run(get_tools(client))

            for tool in tools:
                description = tool.description.replace("\n", "<br>").strip()
                st.markdown(f"""
                | **Tool Name**    | **Description** |
                |------------------|-----------------|
                | {tool.name}           | {description}   |""")

