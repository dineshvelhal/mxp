import streamlit as st

from lib.common_icons import SERVER_ICON, HOME_ICON, TROUBLESHOOT_ICON, PLAY_ICON, TEST_ICON, DOCS_ICON

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

functional_test_page = st.Page("app_pages/functional_test_page.py",
                              title="Functional Test",
                              icon=TEST_ICON)

generate_docs_page = st.Page("app_pages/generate_docs_page.py",
                             title="Generate Server Documentation",
                             icon=DOCS_ICON)


def pages():
    return {
        "Home": [about_page, manage_servers_page, ],
        "Explore Server Capabilities": [inspect_server_page, playground_page],
        "Test MCP Server": [functional_test_page],
        "Documentation": [generate_docs_page],
    }