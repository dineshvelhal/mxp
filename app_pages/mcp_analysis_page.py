import asyncio
import logging
import pandas as pd
import streamlit as st

from lib.mcp_lib import populate_sse_mcp_server_capabilities, get_stdio_mcp_server_capabilities
from lib.st_lib import display_mcp_summary, set_current_page

LOG = logging.getLogger(__name__)
LOG.info("Starting High Level Evaluation page")

set_current_page("mcp_analysis_page")

st.subheader(":material/verified: High Level Evaluation")

c1, c2, c3 = st.columns(3)
with c2:
    st.image("images/WIP.png", width=200)