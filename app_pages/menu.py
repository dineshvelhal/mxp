import streamlit as st

home_page = st.Page("app_pages/about_page.py", title="About", icon="🏠")
mcp_explore_page = st.Page("app_pages/mcp_explore_page.py", title="MCP Explorer", icon="🔍")
mcp_analysis_page = st.Page("app_pages/mcp_analysis_page.py", title="High Level Evaluation", icon="📊")
functional_testing_page = st.Page("app_pages/functional_testing_page.py", title="Functional Testing", icon="🧪")

def pages():
    return {
        "Home": [home_page],
        "MCP Server": [mcp_explore_page, mcp_analysis_page, functional_testing_page],
    }