import streamlit as st

home_page = st.Page("app_pages/about_page.py", title="Home", icon=":material/home:")
mcp_explore_page = st.Page("app_pages/mcp_explore_page.py", title="MCP Explorer", icon=":material/psychology:")

def pages():
    return {
        "Home": [home_page],
        "MCP": [mcp_explore_page],
    }