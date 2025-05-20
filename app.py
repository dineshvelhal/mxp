import logging
import streamlit as st

from app_pages.menu import pages
from lib.st_lib import configure_page, configure_sidebar, initialize_mcp_metadata

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s][%(levelname)s][%(name)-15s:%(lineno)4d] %(message)s',
    # datefmt='%H:%M:%S,%f',
    handlers=[logging.StreamHandler()]  # Log to console
)

LOG = logging.getLogger(__name__)

LOG.info("Started the app...")

initialize_mcp_metadata()

configure_page()
configure_sidebar()

st.navigation(pages=pages(), expanded=True, position="sidebar").run()