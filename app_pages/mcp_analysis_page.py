import logging

import pandas as pd
import streamlit as st

from lib.openai_lib import get_tool_intent_check, get_tool_input_check, get_tool_ret_val_check, \
    get_tool_err_ret_val_check, \
    get_annotations_check
from lib.st_lib import set_current_page, display_mcp_header, get_json_from_dict

LOG = logging.getLogger(__name__)
LOG.info("Starting High Level Evaluation page")

set_current_page("mcp_analysis_page")

# st.subheader(":material/verified: High Level Evaluation")

if not st.session_state.mcp_metadata['transport_type']:
    st.info("ℹ️ Please load the MCP server details on the MCP Explorer page")
    st.stop()

display_mcp_header()





if st.button("Evaluate", type="primary"):
    st.markdown("#### :green-background[💡 High Level Recommendations]")
    if st.session_state.mcp_metadata['transport_type'] == "STDIO":
        if st.session_state.mcp_metadata['command'] == "npx":
            if st.session_state.mcp_metadata['command_args'][0] == "mcp-remote": # remote execution
                if st.session_state.mcp_metadata['command_args'][1].startswith("http:"):
                    st.markdown("""
                    | **Area**         | **Status** | **Recommendation** |
                    |------------------|------------|---------------------|
                    | **Security**     | 🟥         | The **Server URL** is not secure. Please use a secure URL (https://) to ensure data security. |
                    """)
                else:
                    st.markdown("""
                    | **Area**         | **Status** | **Recommendation** |
                    |------------------|------------|---------------------|
                    | **Security**     | ✅         | The **Server URL** is secure. No action required. |
                    """)
            else: # local execution
                st.markdown("""
                | **Area**         | **Status** | **Recommendation** |
                |------------------|------------|---------------------|
                | **Security**     | ✅         | As this is a **local execution** there is no security recommendation! |""")

    elif st.session_state.mcp_metadata['transport_type'] == "SSE":
        if st.session_state.mcp_metadata['url'].startswith("http:"):
            st.markdown("""
            | **Area**         | **Status** | **Recommendation** |
            |------------------|------------|---------------------|
            | **Security**     | 🟥         | The **Server URL** is not secure. Please use a secure URL (https://) to ensure data security. |
            """)
        else:
            st.markdown("""
            | **Area**         | **Status** | **Recommendation** |
            |------------------|------------|---------------------|
            | **Security**     | ✅         | The **Server URL** is secure. No action required. |
            """)

    st.markdown("#### :green-background[🛠️ Interface Evaluation of Supplied Tools]")
    tool_evaluation = []

    with st.spinner("Evaluating tools...", show_time=True):
        for tool in st.session_state.mcp_metadata['tools']:
            tool_description = tool['Description']
            tool_name = tool['Name']
            tool_input_schema = get_json_from_dict(tool['InputSchema'])
            tool_model_json = tool['Model_json']

            annotation_check = get_annotations_check(tool_model_json)
            intent_check = get_tool_intent_check(tool_name, tool_description)
            input_check = get_tool_input_check(tool_description, tool_input_schema)
            return_value_check = get_tool_ret_val_check(tool_description)
            err_ret_value_check = get_tool_err_ret_val_check(tool_description)

            tool_record = {
                "Tool Name": tool_name,
                "Intent Check": intent_check,
                "Input Check": input_check,
                "Response Check": return_value_check,
                "Error Response Check": err_ret_value_check,
                "Annotations Check": annotation_check
            }
            tool_evaluation.append(tool_record)

    df = pd.DataFrame(tool_evaluation)
    styled_df = df.style.applymap(lambda x: 'background-color: lightgreen' if x == "PASS" else 'background-color: #ffcccb' if x == "FAIL" else '',
                                  subset=["Intent Check", "Input Check", "Response Check", "Error Response Check"])
    styled_df1 = styled_df.applymap(lambda x: 'background-color: lightgreen' if x == "FULL"
                                                else 'background-color: #ffcccb' if x == "NIL"
                                                else 'background-color: #FFFF99' if x == "PARTIAL"
                                                else '',
                                    subset=["Annotations Check"])

    st.dataframe(styled_df1, use_container_width=True, hide_index=True, height=300)


