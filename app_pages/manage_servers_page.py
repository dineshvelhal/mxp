import asyncio
import logging
import pandas as pd
import streamlit as st

from lib.fastmcp_lib import test_selected_server
from lib.mcp_lib import populate_sse_mcp_server_capabilities, populate_stdio_mcp_server_capabilities
from lib.server_lib import get_servers, save_server_in_file, delete_server
from lib.st_lib import display_mcp_summary, set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting Manage Servers page")

set_current_page("manage_servers_page")

st.subheader(":material/lan: Manage MCP Servers")

servers = get_servers()
df = pd.DataFrame(servers, columns=["NAME", "TRANSPORT_TYPE", "URL"])

st.write("##### Selected MCP Server")

c1, c2, c3, c4, c5, c6 = st.columns([4, 3, 6, 4, 4, 4], vertical_alignment="bottom")
with c1:
    selected_server_name = st.text_input("Server Name",
                                         value=st.session_state.mcp_metadata.get("name", ""),
                                         help="**Name of the MCP server**. It can be any name that you want to give to the server.",)
with c2:
    selected_transport_type = st.text_input("Type",
                                            value=st.session_state.mcp_metadata.get("transport_type", ""),
                                            help="Transport type is how client communicates with the server. "
                                                 "It can be either **SSE** or **Streamable-HTTP**.")
with c3:
    selected_url = st.text_input("Server URL",
                                 value=st.session_state.mcp_metadata.get("url", ""),
                                 help="**URL of the MCP server**. It can be either a local URL or a remote URL.")

with c4:
    if selected_transport_type:
        if st.button("Test Server", icon=":material/task_alt:", type="primary"):
            try:
                asyncio.run(test_selected_server(selected_transport_type, selected_url))
                st.toast("Server is reachable and operational.", icon="✅")
            except Exception as e:
                st.toast(f"**Connection failed**: {e}", icon="🚨")
                # st.error(f"Error testing server: {e}", icon="🚨")
with c5:
    if selected_transport_type:
        if st.button("Save Server", type="primary", icon=":material/save:",):
            st.session_state.mcp_metadata["name"] = selected_server_name
            st.session_state.mcp_metadata["transport_type"] = selected_transport_type
            st.session_state.mcp_metadata["url"] = selected_url

            try:
                save_server_in_file(selected_server_name, selected_transport_type, selected_url)
                st.rerun()
            except ValueError as e:
                st.toast(f"Error saving server: {e}", icon="🚨")
                # st.error(f"Error saving server: {e}", icon="🚨")

with c6:
    if selected_transport_type:
        if st.button("Delete Server", type="tertiary", icon=":material/delete:"):
            delete_record = {"NAME": selected_server_name,
                             "TRANSPORT_TYPE": selected_transport_type,
                             "URL": selected_url}

            if delete_record in servers:
                st.session_state.mcp_metadata["name"] = ""
                st.session_state.mcp_metadata["transport_type"] = ""
                st.session_state.mcp_metadata["url"] = ""
                delete_server(selected_server_name)
                st.rerun()
            else:
                st.toast("Server not found in saved servers.", icon="🚨")

st.write("##### Saved MCP Servers")
event = st.dataframe(df,
                     use_container_width=True,
                     hide_index=True,
                     selection_mode="single-row",
                     on_select="rerun",
                     column_config={
                         "URL": st.column_config.LinkColumn("URL",
                                                            help="Click to open the server URL in a new tab",),
                     })

if event.selection.rows:
    if st.button("Load Selected Server", type="primary", icon=":material/arrow_circle_right:"):
        selection = event.selection.rows
        selected_df = df.iloc[selection]

        # iterate over selected_df
        for index, row in selected_df.iterrows():
            st.session_state.mcp_metadata["name"] = row["NAME"]
            st.session_state.mcp_metadata["transport_type"] = row["TRANSPORT_TYPE"]
            st.session_state.mcp_metadata["url"] = row["URL"]
            st.rerun()





