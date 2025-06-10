import logging

import streamlit as st

from lib.st_lib import set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting About page")

set_current_page("about_page")

# st.subheader("MCP Certify")
st.html("""<h1 style="font-family: 'Orbitron', sans-serif; font-size: 24px; color: #F85D13;">MCP - Explorer</h1>""")

# with st.container(border=True):
st.markdown("""
    ### Explore MCP Server capabilities and validate its interfaces for missing schema definitions!
    
    **[Model Context Protocol (MCP)](https://modelcontextprotocol.io/)** enables **AI agents** to **communicate** with each other and with the world around them by providing a standardized way.
    
    It's vitally important to **test, evaluate and certify** the **MCP Servers** provided by 3rd party or developed in-house on various criteria
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.image("images/banner1.png", use_container_width=True)
with c2:
    st.image("images/banner2.png", use_container_width=True)
with c3:
    st.image("images/banner3.png", use_container_width=True)

