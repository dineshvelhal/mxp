import base64
import json
import logging
import os
from pathlib import Path

import streamlit as st

log = logging.getLogger(__name__)


def set_current_page(page_name: str):
    """ Detects when page switch happens and runs the page switch code"""
    log.info('inside set_current_page')

    if 'current_page' not in st.session_state:
        log.info('Most probably application is initializing or the current page is being refreshed')
        st.session_state.current_page = page_name
    else:
        if st.session_state.current_page == page_name:
            log.info(f'page {st.session_state.current_page} is reloading')
        else:
            log.info(f'Switching page from [{st.session_state.current_page}] to [{page_name}]')
            st.session_state.current_page = page_name


def configure_sidebar():
    """Adds a sidebar and populates the navigation menu"""
    add_app_logo('images/logo.png')
    # st.logo("images/logo.png", size="large", icon_image="images/logo.png")
    with st.sidebar:
        st.markdown('''
## `Version: 0.1`
## `Contact: Dinesh Velhal`''')



def add_app_logo(image_file: str):
    """Adds logo from the image file to the app """
    image_path = os.path.abspath(image_file)

    logo = f"url(data:image/png;base64,{base64.b64encode(Path(image_path).read_bytes()).decode()})"
    st.markdown(
        f"""
            <style>
                [data-testid="stSidebarContent"] {{
                    background-image: {logo};
                    background-repeat: no-repeat;
                    padding-top: {80}px;
                    background-position: 20px 20px;
                }}
            </style>
            """,
        unsafe_allow_html=True,
    )


def configure_page():
    st.set_page_config(layout="wide")


def set_compact_cols():
    st.markdown("""
                <style>
                    div[data-testid="column"] {
                        width: fit-content !important;
                        flex: unset;
                    }
                    div[data-testid="column"] * {
                        width: fit-content !important;
                    }
                </style>
                """, unsafe_allow_html=True)


def initialize_mcp_metadata():
    """Initialize the dict object that holds all MCP details"""
    if "mcp_metadata" not in st.session_state:
        st.session_state.mcp_metadata = {
            "transport_type": None,
            "command": None,
            "args": [],
            "url": "",
            "tools": [],
            "prompts": [],
            "resources": []
        }


def display_mcp_header():
    st.markdown("#### :blue-background[🧾 MCP Server Summary]")
    # st.markdown(f"Transport Type: :blue[{st.session_state.mcp_metadata['transport_type']}]")

    if st.session_state.mcp_metadata['transport_type'] == "STDIO":
        st.markdown(f"""
                | Transport Type | Command | Command Arguments |
                |----------------|---------|------------------|
                | {st.session_state.mcp_metadata['transport_type']} | {st.session_state.mcp_metadata['command']} | {st.session_state.mcp_metadata['command_args']} |
                """)
        # st.markdown(f"Command: :blue[{st.session_state.mcp_metadata["command"]}]")
        # st.markdown(f"Command Arguments: :blue[{st.session_state.mcp_metadata["command_args"]}]")
    else:
        st.markdown(f"""
                | Transport Type | Server URL |
                |----------------|------------|
                | {st.session_state.mcp_metadata['transport_type']} | {st.session_state.mcp_metadata["url"]} |
                """)
        # st.markdown(f"Server URL: :blue[{st.session_state.mcp_metadata["url"]}]")


def display_mcp_summary():
    if "mcp_metadata" not in st.session_state:
        st.error("MCP Server is not loaded. Please load server details and try again!")
    else:

        display_mcp_header()

        st.markdown("#### :blue-background[🚀 Supplied Capabilities]")

        tab_tools, tab_resources, tab_prompts = st.tabs(["🛠️ Tools", "📦 Resources", "📝 Prompts"])

        with tab_tools:
            for tool in st.session_state.mcp_metadata["tools"]:
                # with st.container(border=True):
                st.markdown(f"##### 🛠️ Tool Name: :blue[{tool['Name']}]")
                # st.markdown(f"**Description**")
                with st.expander("Expand to see tool details", expanded=False):
                    st.code(f"""DESCRIPTION
---------------
{tool["Description"]}"""
                            , language="text", wrap_lines=True)

                    st.markdown("###### :blue-background[📥 Input Arguments]")

                    st.markdown(dict_to_markdown_table(tool["InputSchema"]))
                    st.markdown("###### :blue-background[🔖 Annotations]")
                    st.markdown(annotations_to_markdown_table(tool["Model_json"]))

        with tab_resources:
            st.image("images/WIP.png", width=200)

        with tab_prompts:
            st.image("images/WIP.png", width=200)


def dict_to_markdown_table(inputSchema: dict) -> str:
    """
    Convert a DICT to a markdown table.
    :param json_str:
    :return:
    """
    data = inputSchema
    properties = data.get("properties", {})
    required_fields = set(data.get("required", []))

    # Header of the markdown table
    table = ["| Argument |  Type | Default Value  | Required? |",
             "|----------|-------|----------------|-----------|"]

    for arg_name, attrs in properties.items():
        arg_type = attrs.get("type", "")
        default_val = attrs.get("default", "")
        required = "Yes" if arg_name in required_fields and not default_val else "No"
        table.append(f"| {arg_name}   | {arg_type} | {str(default_val):<14} |    {required}    |")

    return "\n".join(table)

def annotations_to_markdown_table(model: str) -> str:
    """
    Convert a DICT to a markdown table.
    :param json_str:
    :return:
    """

    model_json = json.loads(model)
    annotations = model_json.get("annotations", None)

    if annotations:
        title = annotations.get("title", "")
        read_only_hint = annotations.get("readOnlyHint", "")
        destructive_hint = annotations.get("destructiveHint", "")
        idempotent_hint = annotations.get("idempotentHint", "")
        open_world_hint = annotations.get("openWorldHint", "")

        # Header of the markdown table that shows annotations
        table = ["| Title    |  readOnlyHint | Destructive Hint | Idempotent Hint | Open World Hint |",
                 "|----------|----------------|------------------|-----------------|-----------------|"]

        table_row = f"| {title} | {read_only_hint} | {destructive_hint} | {idempotent_hint} | {open_world_hint} |"
        table.append(table_row)
        return "\n".join(table)
    else:
        return "No Annotations Found"


def get_json_from_dict(d: dict):
    """
    Return json string from dict object
    :param d: dict object
    """
    if isinstance(d, dict):
        return json.dumps(d, indent=4)
    else:
        raise TypeError("Input is not a dictionary")