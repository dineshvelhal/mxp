import logging

import streamlit as st

LOG = logging.getLogger(__name__)
LOG.info("Starting About page")

# st.subheader("MCP Certify")
st.html("""<h1 style="font-family: 'Orbitron', sans-serif;">MCP - Certify</h1>""")

with st.container(border=True):
    st.markdown("""
##### Why MCP Server Evaluation Matters

As AI systems increasingly rely on real-time contextual data to deliver meaningful and safe responses, the **Model Context Protocol (MCP)** has become a critical layer in modern AI infrastructure. 

**Evaluating, testing & certifying the MCP servers** ensures they handle context reliably, securely, and in strict adherence to the protocol. Without rigorous validation, even minor inconsistencies can lead to poor performance, erratic behavior, or security risks. A well-tested MCP server provides confidence to developers and enterprises alike—guaranteeing seamless integration, robust interoperability, and trust at scale.


    """)