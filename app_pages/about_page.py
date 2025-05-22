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
### Getting ready for the Agentic Revolution!

**Model Context Protocol (MCP)** enables **AI agents** to **communicate** with each other and with the world around them by providing a standardized way .

Thus it's vitally important to **test, evaluate and certify** the **MCP Servers** provided by 3rd party or developed in-house on various criteria such as

| **Criteria**                | **Description**                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| **Functionality**           | Does the server perform its intended functions correctly?                      |
| **Performance**             | Does the server perform under load and handles resource cleanup efficiently?   |
| **Security**                | Is the server secure against common vulnerabilities?                           |
| **Gen AI Interoperability** | Does the server interact effectively with LLMs?                            |
| **Usability**               | Is the server easy to use and understand?                                      |

**MCP-Certify** performs the above tests and provides a **certification** for the MCP server. The certification is based on the results of the tests and is intended to provide assurance to users that the server meets certain standards of quality and reliability.
    """)