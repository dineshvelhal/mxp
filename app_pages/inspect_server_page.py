import asyncio
import logging

import numpy as np
import pandas as pd
import streamlit as st

from lib.common_icons import TOOL_ICON, RESOURCE_ICON, PROMPT_ICON, INPUT_ICON, INFO_ICON, OUTPUT_ICON, ANNOTATION_ICON, \
    ANALYSIS_ICON, LIGHTBULB_ICON, GAPS_ICON, TROUBLESHOOT_ICON
from lib.fastmcp_lib import get_tools, get_client
# from lib.mcp_lib import populate_sse_mcp_server_capabilities, populate_stdio_mcp_server_capabilities
from lib.st_lib import set_current_page, show_info, h5, h6, h4, show_error
from lib.tool_lib import get_input_schema, get_output_schema, get_annotations, make_analysis_colorful

LOG = logging.getLogger(__name__)
LOG.info("Starting MCP Explore page")

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

set_current_page("inspect_server_page")

if not st.session_state.mcp_metadata.get("transport_type", ""):
    show_info("Please set the **Current MCP server** on the **Manage Servers** page.")
    LOG.info("No MCP server selected. Stopping further execution.")
    st.stop()

transport_type = st.session_state.mcp_metadata.get("transport_type", "")
server_name = st.session_state.mcp_metadata.get("name", "")
server_url = st.session_state.mcp_metadata.get("url", "")
# if transport_type == "SSE":
#     sse_url = st.session_state.mcp_metadata.get("url", "")
# elif transport_type == "Streamable-HTTP":
#     s_http_url = st.session_state.mcp_metadata.get("url", "")

st.subheader(f"{TROUBLESHOOT_ICON} Inspect MCP Server capabilities [Name: `{server_name}`]")

if st.button(f"Load Server Details",
             key="load_mcp_details",
             help="Click to load MCP supported tools",
             type="primary"):
    LOG.info("Load MCP server details button clicked")
    # with st.spinner("Loading MCP server details...", show_time=True):

    tabTools, tabResources, tabPrompts = st.tabs([f"{TOOL_ICON} Tools", f"{RESOURCE_ICON} Resources", f"{PROMPT_ICON} Prompts"])

    with tabTools:
        # mcp_client = asyncio.run(get_client())
        mcp_tools, status_message = asyncio.run(get_tools())

        if len(mcp_tools) == 0:
            st.error(f"No tools found on the MCP server. Message from server: {status_message}")
            LOG.error(f"No tools found on the MCP server. Message from server: {status_message}")
            st.stop()

        # st.success(f"Successfully fetched {len(mcp_tools)} tools from the MCP server.")
        LOG.info(f"Successfully fetched {len(mcp_tools)} tools from the MCP server.")

        # This section holds summary & recommendations
        with st.container(border=True):
            observations = []
            summary_heading_slot = st.empty()
            summary_slot = st.empty()
            summary_recommendations_slot = st.empty()

        with st.container(border=True):
            h5(f"{GAPS_ICON} Tool-level Gaps Analysis")
            for tool in mcp_tools:
                with st.status(f"{TOOL_ICON} Inspecting tool: `{tool['NAME']}`...",) as status:
                    tool_observations = {"NAME": tool["NAME"]}

                    h5(f"{TOOL_ICON} {tool['NAME']}")
                    h6(f"{INFO_ICON} Description")
                    if tool.get("DESCRIPTION", ""):
                        st.code(tool["DESCRIPTION"], language="text", wrap_lines=True)
                        tool_observations["DESCRIPTION"] = "OK"
                    else:
                        show_error("No description found for this tool.")
                        tool_observations["DESCRIPTION"] = "MISSING"

                    h6(f"{INPUT_ICON} Input Parameters")
                    try:
                        input_schema, result = get_input_schema(tool)
                        st.dataframe(input_schema, hide_index=True)
                        tool_observations["INPUT SCHEMA"] = result
                    except ValueError as e:
                        st.error(f"No input parameters found!: `[{e}]`")
                        LOG.error(f"No input parameters found!: [{e}]")
                        tool_observations["INPUT SCHEMA"] = "NA"

                    h6(f"{OUTPUT_ICON} Output Parameters")
                    try:
                        output_schema = get_output_schema(tool)
                        st.dataframe(output_schema, hide_index=True)
                        tool_observations["OUTPUT SCHEMA"] = "OK"
                    except ValueError as e:
                        st.error(f"No output parameters found!: `[{e}]`")
                        LOG.error(f"No output parameters found!: [{e}]")
                        tool_observations["OUTPUT SCHEMA"] = "MISSING"

                    h6(f"{ANNOTATION_ICON} Annotations")
                    try:
                        annotations, result = get_annotations(tool)
                        st.dataframe(annotations, hide_index=True)
                        tool_observations["ANNOTATIONS"] = result
                    except ValueError as e:
                        st.error(f"No annotations found!: `[{e}]`")
                        LOG.error(f"No annotations found!: [{e}]")
                        tool_observations["ANNOTATIONS"] = "MISSING"

                    status.update(label=f"{TOOL_ICON} {tool['NAME']}", state="complete", expanded=False)
                    observations.append(tool_observations)

        # Display summary of observations
        summary_heading_slot.markdown(f"#### {ANALYSIS_ICON} Gap Analysis")
        df = pd.DataFrame(observations)
        stylized_df = make_analysis_colorful(df)
        summary_slot.dataframe(stylized_df, hide_index=True)
        summary_recommendations_slot.markdown(f"""
#### {LIGHTBULB_ICON} Why it matters?
The analysis above provides insights into the completeness and quality of the tools available on the MCP server.
 - :red-background[**Missing Descriptions**]: LLM/Agent may get the tool intent wrong or not understand its purpose during tool decision step
- :red-background[**Missing/Incomplete Input Schema**]: LLM/Agent may not be able to provide the correct input parameters for the tool
- :red-background[**Missing/Incomplete Output Schema**]: It may be the case that MCP server is not compliant with latest **MCP Specification wef 2025-06-18**
- :red-background[**Missing Annotations**]: Tool annotations provide additional metadata about a tool’s behavior, helping clients understand how to present and manage tools. Though not required in tool-decision step, missing annotations can lead to confusion in tool usage.

###### See below, what's missing/incorrect at the tool level.
        """)


    with tabResources:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c3:
            st.image("images/wip.png", use_container_width=True)

    with tabPrompts:
        c21, c22, c23, c24, c25 = st.columns(5)
        with c23:
            st.image("images/wip.png", use_container_width=True)