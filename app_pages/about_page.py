import logging

import streamlit as st

from lib.st_lib import set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting About page")

set_current_page("about_page")

# st.subheader("MCP Certify")
st.html("""<div style="font-family: 'Space Grotesk', sans-serif; font-size: 35px; font-weight: bold; color: #00A1DA;">MCP Deep-View</div>""")

# with st.container(border=True):
st.markdown("""
About MCP Deep-Eval
""")

# c1, c2, c3 = st.columns(3)
#
# with c1:
#     st.image("images/banner1.png", use_container_width=True)
# with c2:
#     st.image("images/banner2.png", use_container_width=True)
# with c3:
#     st.image("images/banner3.png", use_container_width=True)

