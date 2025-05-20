import logging

import streamlit as st

LOG = logging.getLogger(__name__)
LOG.info("Starting About page")

st.title("About MCP Explorer")

with st.container(border=True):
    st.markdown("""
Explore MCP Servers and their capabilities, strengths and weaknesses.

    """)