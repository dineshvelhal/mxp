import logging

import streamlit as st

from lib.st_lib import set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting About page")

set_current_page("about_page")

# st.subheader("MCP Certify")
st.html("""<h1 style="font-family: 'Orbitron', sans-serif; font-size: 24px;">MCP - Certify</h1>""")

# with st.container(border=True):
st.markdown("""
    ### Certify MCP Servers before use in your organization!
    
    **Model Context Protocol (MCP)** enables **AI agents** to **communicate** with each other and with the world around them by providing a standardized way .
    
    It's vitally important to **test, evaluate and certify** the **MCP Servers** provided by 3rd party or developed in-house on various criteria
""")

c1, c2, c3, c4 = st.columns([2, 5, 5, 2])

with c2:
    st.image("images/banner1.png", use_container_width=True)

with c3:
    st.image("images/banner2.png", use_container_width=True)

st.markdown("""
**MCP-Certify** performs the above tests and provides a **certification** for the MCP server. The certification is based on the results of the tests and is intended to provide assurance to users that the server meets certain standards of quality and reliability.
    """)