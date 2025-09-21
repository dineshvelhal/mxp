import asyncio
import logging
import os
from http.client import responses

import streamlit as st

from lib.common_icons import TEST_ICON, SERVER_ICON
from lib.fastmcp_lib import get_tools
from lib.openai_lib import get_test_cases
from lib.st_lib import set_current_page, show_info
from lib.tool_lib import get_input_schema

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

st.subheader(f"{TEST_ICON} Functional Testing [`{server_name}`]")

with st.spinner("Fetching tools from the MCP server...", show_time=True):
    mcp_tools, status_message = asyncio.run(get_tools())

if mcp_tools:
    tool_names = [tool["NAME"] for tool in mcp_tools]
    tool_names.insert(0, "")

    selected_tool_name = st.selectbox(
        "Select a tool to test",
        tool_names,
        index=0,
        help="Select a tool to test its functionality against the current MCP server."
    )

    if selected_tool_name == "":
        show_info("Please select a tool to generate tests.")
        LOG.info("No tool selected. Stopping further execution.")
        st.stop()

    selected_tool = [tool for tool in mcp_tools if tool["NAME"] == selected_tool_name][0]
    #
    # st.markdown(f"###### Selected Tool: `{selected_tool_name}`")
    # st.markdown(f"**Description:** {selected_tool.get('DESCRIPTION', 'No description available.')}")

    st.markdown(f"""
    | Selected Tool | Description |
    |---------------|-------------|
    | {selected_tool_name} | {selected_tool.get('DESCRIPTION', 'No description available.')} |
    """)

    input_schema_df, result = get_input_schema(selected_tool)
    st.dataframe(input_schema_df, hide_index=True)

    # st.write("**Input Schema JSON:**")
    input_schema = selected_tool.get("INPUT_SCHEMA", {})

    negative_tests_prompt = f"""
    You are an expert software tester with a lot of experience in writing tests using pytest.
    
    Given the JSON schema enclosed in <schema>...</schema>, generate a set of NEGATIVE test cases.
    You must use the `pytest` framework for writing the tests and must generate the parameterized tests using `@pytest.mark.parametrize`.
    
    Assume that a FastMCP client is instantiated as `client` and is available for use in the tests.
    Tool call is made as `asyncio.run(client.call_tool`.
    
    Example: A tool named `get_current_weather(city: str)` would be called as
    `asyncio.run(client.call_tool("get_current_weather", {{"city": "London"}}))`.
    
    You must return only the pytest tests without adding any niceties or explanations and without adding ````python` or any other code block tags.

    <schema>
    {input_schema}
    </schema>
    """

    st.markdown("##### Negative Test Cases")
    with st.spinner("Generating negative test cases...", show_time=True):
        response = get_test_cases(negative_tests_prompt)

        # with st.container(border=True):
        st.code(response, language="python")

    positive_tests_prompt = f"""
    You are an expert software tester with a lot of experience in writing tests using pytest.

    Given the JSON schema enclosed in <schema>...</schema>, generate a set of POSITIVE test cases.
    You must use the `pytest` framework for writing the tests and must generate the parameterized tests using `@pytest.mark.parametrize`.

    Assume that a FastMCP client is instantiated as `client` and is available for use in the tests.
    Tool call is made as `asyncio.run(client.call_tool`.

    Example: A tool named `get_current_weather(city: str)` would be called as
    `asyncio.run(client.call_tool("get_current_weather", {{"city": "London"}}))`.

    You must return only the pytest tests without adding any niceties or explanations and without adding ````python` or any other code block tags.

    <schema>
    {input_schema}
    </schema>
    """

    st.markdown("##### Positive Test Cases")
    with st.spinner("Generating positive test cases...", show_time=True):
        response = get_test_cases(positive_tests_prompt)

    # with st.container(border=True):
    st.code(response, language="python")




