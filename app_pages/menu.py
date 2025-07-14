import streamlit as st

from lib.common_icons import SERVER_ICON, HOME_ICON, TROUBLESHOOT_ICON, PLAY_ICON

about_page = st.Page("app_pages/about_page.py",
                     title="About",
                     icon=HOME_ICON,
                     default=True)

manage_servers_page = st.Page("app_pages/manage_servers_page.py",
                              title="Manage Servers",
                              icon=SERVER_ICON)

inspect_server_page = st.Page("app_pages/inspect_server_page.py",
                              title="Inspect Server Capabilities",
                              icon=TROUBLESHOOT_ICON)

playground_page = st.Page("app_pages/playground_page.py",
                          title="Playground",
                          icon=PLAY_ICON)

def pages():
    return {
        "Home": [about_page],
        "MCP": [manage_servers_page, inspect_server_page, playground_page],
    }