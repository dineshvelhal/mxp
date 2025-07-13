import asyncio
import logging
import time

import pandas as pd
import streamlit as st

from lib.common_icons import SERVER_ICON
from lib.fastmcp_lib import test_selected_server
from lib.server_lib import get_servers, save_server_in_file, delete_server
from lib.st_lib import set_current_page, set_compact_cols, show_warning, show_info, show_success, \
    reset_mcp_metadata, confirm_yes_no_dialog, show_error, h6

LOG = logging.getLogger(__name__)
LOG.info("Starting Manage Servers page")

set_compact_cols()

set_current_page("manage_servers_page")

st.subheader(f"{SERVER_ICON} Manage MCP Servers")

servers = get_servers()
df = pd.DataFrame(servers).transpose()
if df.empty:
    show_warning("No MCP servers found. Please add a new server.")

tab_main, tab_add_server = st.tabs(["Manage Existing Servers", "Add New Server"])

with tab_main:
    saved_servers = st.dataframe(df, use_container_width=True, hide_index=False, selection_mode="single-row", on_select="rerun")

    h6(f"Current Active MCP Server: `{st.session_state['mcp_metadata'].get('name', 'None')}`")

    server_selected = False
    try:
        selected_row_index = saved_servers.selection["rows"][0]
        selected_index = df.index[selected_row_index]
        selected_row = df.iloc[selected_row_index]
        # st.write(f"Selected Server: **{selected_index}**")
        server_selected = True
        # selected_index contains the index value, selected_row contains all column values
    except (KeyError, IndexError) as e:
        show_warning(f"To change current active server, you need to select a server from above Grid. `[{e}]`")

    if server_selected:
        c1, c2, c3 = st.columns(3, vertical_alignment="bottom")
        with c1:
            set_current_server_button_clicked = st.button("Set as Current", type="primary", icon=":material/priority:")
            LOG.info(f"Set current server button clicked")
        with c2:
            delete_server_button_clicked = st.button("Delete Selected", type="secondary", icon=":material/delete:")
            LOG.info(f"Delete server button clicked")
        with c3:
            test_server_button_clicked = st.button("Test Server", type="secondary", icon=":material/arrow_right:")
            LOG.info(f"Test server button clicked")


        if set_current_server_button_clicked:
            st.session_state.mcp_metadata["name"] = selected_index
            st.session_state.mcp_metadata["transport_type"] = selected_row["TRANSPORT_TYPE"]
            st.session_state.mcp_metadata["url"] = selected_row["URL"]
            show_success(f"[{selected_index}] is set as the current MCP server.")
            LOG.info(f"Current MCP server set to: {selected_index}")

        if delete_server_button_clicked:
            try:
                delete_server(selected_index)
                reset_mcp_metadata()
                show_success(f"Server [{selected_index}] deleted successfully.")
                LOG.info(f"Server [{selected_index}] deleted successfully.")
                time.sleep(3)
                st.rerun()
            except Exception as e:
                show_warning(f"Error deleting server: {e}")
                LOG.error(f"Error deleting server [{selected_index}]: {e}")

        if test_server_button_clicked:
            server_available, server_error = asyncio.run(test_selected_server(selected_row["TRANSPORT_TYPE"], selected_row["URL"]))
            if server_available:
                show_success(f"Server [{selected_index}] is reachable.")
                LOG.info(f"Server [{selected_index}] is reachable.")
            else:
                show_error(f"Error connecting to server [{selected_index}]: {server_error}")
                LOG.error(f"Error connecting to server [{selected_index}]: {server_error}")

with tab_add_server:
    st.markdown("**Add New MCP Server**")

    with st.form("add_server_form", clear_on_submit=True):
        server_name = st.text_input("Server Name", placeholder="Enter a name for the server")
        transport_type = st.selectbox("Transport Type", ["SSE", "Streamable-HTTP"], index=0)
        url = st.text_input("Server URL", placeholder="Enter the server URL")
        # command = st.text_input("Command", placeholder="Enter the command to run MCP server")
        # command_args = st.text_input("Command Arguments", placeholder="Enter command arguments (comma separated)")

        submit_button = st.form_submit_button("Add Server")

        if submit_button:
            if not server_name or not url:
                show_warning("Please fill in all required fields.")
                LOG.warning("Server name or URL is empty.")
            else:
                try:
                    save_server_in_file(server_name, transport_type, url)
                    show_success(f"Server [{server_name}] added successfully.")
                    LOG.info(f"Server [{server_name}] added successfully.")
                    time.sleep(5)
                    st.rerun()
                except Exception as e:
                    show_warning(f"Error adding server: {e}")
                    LOG.error(f"Error adding server [{server_name}]: {e}")