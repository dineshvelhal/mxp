import logging
import os

import streamlit as st

from lib.st_lib import set_current_page

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
LOG.info("Starting About page")

set_current_page("about_page")

# st.subheader("MCP Certify")
st.html("""<H1 style="color: #00B0F0;">About MCP Explorer</H1>""", width="content")

# with st.container(border=True):
# st.markdown("""
# About MCP Deep-Eval
# """)

c1, c2, c3 = st.columns(3, vertical_alignment="top", border=True)
with c1:
    st.markdown("""
#### Why test MCP Servers?
- It's a piece of software (Obviously! 😊)
- **Higher risk** due to autonomous use by AI Agents
- To ensure they **integrate** well with other systems
- Ensure they meet **Org standards and policies**
- Ensure they **perform well under load**
 """)
with c2:
    st.markdown("""
#### MCP Deep-View Features
- **Inspect** MCP server capabilities
- **Gap analysis** of Server Metadata (input schema, annotations etc.)
- **Integration testing** with LLMs and Agents
- Generate **human-readable** MCP server **documentation**
- Generate **functional tests** for MCP servers
""")

with c3:
    st.markdown("""
#### Currently supports
- Transport types
    - **SSE**
    - **Streamable HTTP**
- Servers hosted **locally**
- **Remote Servers** from internet
- Servers developed in **any language**
- Latest MCP protocol **revision dt. 2025-06-18**
""")

