import logging
import streamlit as st
from lib.st_lib import display_mcp_summary, set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting Functional Testing page")

set_current_page("functional_testing_page")

st.subheader(":material/verified: Functional Testing")

c1, c2, c3 = st.columns(3)
with c2:
    st.image("images/WIP.png", width=200)