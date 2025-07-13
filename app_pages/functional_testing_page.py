import logging

import streamlit as st

from lib.st_lib import set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting Functional Testing page")

set_current_page("functional_testing_page")

st.subheader(":material/verified: Functional Testing")

c1, c2, c3 = st.columns(3)
with c2:
    st.image("images/WIP.png", width=200)

# tool_name_list = [item["Name"] for item in st.session_state.mcp_metadata['tools']]
# selected_tool_name = st.selectbox("Select Tool", options=tool_name_list, index=0,)
#
# if selected_tool_name:
#     tool_description = [item for item in st.session_state.mcp_metadata['tools'] if item["Name"] == selected_tool_name][0]["Description"]
#     tool_input_schema = [item for item in st.session_state.mcp_metadata['tools'] if item["Name"] == selected_tool_name][0]["InputSchema"]
#
#     positive_test_cases = get_positive_test_cases(selected_tool_name, tool_description, tool_input_schema)
#     st.markdown("### Positive Test Cases")
#     st.markdown(positive_test_cases)

