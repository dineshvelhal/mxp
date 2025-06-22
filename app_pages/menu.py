import streamlit as st


home_page = st.Page("app_pages/about_page.py",
                    title="About MCP Deep-Eval",
                    icon=":material/home:",
                    default=True)
manage_servers_page = st.Page("app_pages/manage_servers_page.py",
                              title="Manage Servers",
                              icon=":material/lan:")
mcp_explore_page = st.Page("app_pages/mcp_explore_page.py",
                           title="Inspect Server Capabilities",
                           icon=":material/troubleshoot:")
mcp_analysis_page = st.Page("app_pages/mcp_analysis_page.py",
                            title="Interface Evaluation",
                            icon="🤝")
functional_testing_page = st.Page("app_pages/functional_testing_page.py",
                                  title="Functional Testing",
                                  icon=":material/assignment_turned_in:")
try_with_llm_page = st.Page("app_pages/try_with_llm_page.py",
                            title="Playground",
                            icon=":material/directions_run:")

def pages():
    return {
        "Home": [home_page],
        "MCP": [manage_servers_page, mcp_explore_page, try_with_llm_page],
    }