import asyncio
import json
import logging
import os

import streamlit as st

from lib.common_icons import EXPLORE_ICON, PLAY_ICON, PROMPT_ICON, LLM_ICON, QUESTION_ICON, PLUGIN_ICON, TOOL_ICON, \
    SELECT_ICON, EXECUTE_ICON
from lib.fastmcp_lib import get_client, get_tools, call_tool
from lib.openai_lib import get_llm_tool_selection_response
from lib.st_lib import set_current_page, show_info, show_error, show_success

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
LOG.info("Starting MCP Explore page")

set_current_page("playground_page")

if not st.session_state.mcp_metadata.get("transport_type", ""):
    show_info("Please set the **Current MCP server** on the **Manage Servers** page.")
    LOG.info("No MCP server selected. Stopping further execution.")
    st.stop()

transport_type = st.session_state.mcp_metadata.get("transport_type", "")
server_name = st.session_state.mcp_metadata.get("name", "")
server_url = st.session_state.mcp_metadata.get("url", "")


st.subheader(f"{PLAY_ICON} MCP Playground [`{server_name}`]")

with st.expander("LLM Settings", expanded=False, icon=":material/settings:"):
    c1, c2 = st.columns(2, vertical_alignment="top", gap="large")
    with c1:
        selected_model = st.selectbox("Select LLM Model", ["gpt-4.1-mini", "gpt-4.1", "gpt-5-mini", "gpt-5"],)
        system_prompt = st.text_area("System Prompt",
                                     height=150,
                                     placeholder="Enter system prompt for the LLM",
                                     max_chars=200,
                                     value="You are a helpful assistant. Please answer the questions to the best of your ability.",
                                     help="This is the system prompt that will be sent to the LLM. It sets the context for the conversation.",)
        LOG.info(f"System prompt set: {system_prompt[:50]}...")  # Log first 50 chars for brevity
    with c2:
        max_tokens = st.slider("Max Tokens", min_value=100, max_value=1000, value=300, step=100,
                               help="Maximum number of tokens to generate in the response. Adjust based on your needs.")
        temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1,
                                help="Controls the randomness of the output. Lower values make the output more deterministic, while higher values make it more random.")
        top_p = st.slider("Top P", min_value=0.0, max_value=1.0, value=0.9, step=0.1,
                          help="Controls the diversity of the output by considering only the top P probability mass. A value of 1.0 means no restriction.")
        LOG.info(f"LLM settings - Max Tokens: {max_tokens}, Temperature: {temperature}, Top P: {top_p}")

c21, c22 = st.columns(2, vertical_alignment="bottom", gap="large")
with c21:
    question = st.text_area("Question",
                            height=100,
                            placeholder="Enter your question here",
                            max_chars=200,
                            help="This is the question you want to ask the LLM. It will be processed along with the system prompt.",)
with c22:
    submit_button = st.button("Submit your question", type="primary", icon=QUESTION_ICON)


if submit_button:
    if not question.strip():
        show_error("Please enter a question before submitting.")
        LOG.warning("Submit button clicked without a question.")
    else:
        LOG.info(f"Question submitted: {question[:50]}...")  # Log first 50 chars for brevity

        with st.status(f"{PLUGIN_ICON} Plug-in the MCP Server", expanded=True) as plugin_status:
            data = [{"SERVER NAME": server_name, "SERVER URL": server_url, "TRANSPORT TYPE": transport_type}]
            st.dataframe(data, use_container_width=True, hide_index=True)
            plugin_status.update(label=f"{PLUGIN_ICON} Plug-in the MCP Server", state="complete", expanded=False)


        with st.status(f"{TOOL_ICON} Fetch MCP tools", expanded=True) as tool_list_status:
            tools, tool_status = asyncio.run(get_tools())
            tools_list = []
            for tool in tools:
                record = {"TOOL _NAME": tool["NAME"], "DESCRIPTION": tool["DESCRIPTION"]}
                tools_list.append(record)

            st.write("###### Available Tools")
            st.dataframe(tools_list, use_container_width=True, hide_index=True)
            tool_list_status.update(label=f"{TOOL_ICON} Fetch MCP tools.", state="complete", expanded=False)


        with st.status(f"{SELECT_ICON} Request tool selection by the LLM", expanded=True) as tool_sent_status:
            aoai_tools = [
                {
                    "type": "function",
                    "function": {
                        "name": tool["NAME"],
                        "description": tool["DESCRIPTION"],
                        "parameters": tool["INPUT_SCHEMA"]
                    }
                } for tool in tools
            ]

            aoai_tools_json = json.dumps(aoai_tools, indent=2)
            st.write("##### Details sent to LLM")
            c31, c32 = st.columns(2, vertical_alignment="top")
            with c31:
                st.write("###### System Prompt")
                st.code(system_prompt, language="text", wrap_lines=True, height=100)
            with c32:
                st.write("###### Question")
                st.code(question, language="text", wrap_lines=True, height=100)
            st.write("###### Tools Details")
            st.json(aoai_tools_json, expanded=True)

            tool_sent_status.update(label=f"{SELECT_ICON} Request tool selection by the LLM.", state="complete", expanded=False)

        with st.status(f"{LLM_ICON} Receive Tool Selection by LLM", expanded=True) as llm_response_status:
            try:
                messages = [{"role": "system", "content": system_prompt},
                            {"role": "user", "content": question}]
                message = get_llm_tool_selection_response(
                    model=selected_model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    messages=messages,
                    tools=aoai_tools
                )
            except Exception as e:
                show_error(f"Error getting LLM response: {e}")
                LOG.error(f"Error getting LLM response: {e}")
                llm_response_status.update(label=f":red[Error getting LLM response: {e}]", state="error", expanded=False)
                st.stop()

            if message.content:
                st.write("###### LLM Response")
                st.code(message.content, language="text", wrap_lines=True, height=100)
            if message.tool_calls:
                st.write("###### LLM selected the following tool calls along with arguments:")

                calls = []
                for tool_call in message.tool_calls:
                    call_record = {
                        "TOOL CALL ID": tool_call.id,
                        "TOOL NAME": tool_call.function.name,
                        "TOOL ARGUMENTS": tool_call.function.arguments,
                    }
                    calls.append(call_record)
                st.dataframe(calls, use_container_width=True, hide_index=True)
            else:
                show_info("No tools were selected by the LLM.")
            llm_response_status.update(label=f"{LLM_ICON} Receive Tool Selection by LLM.", state="complete", expanded=False)

        if message.tool_calls:
            with st.status(f"{EXECUTE_ICON} Execute Selected Tools", expanded=True) as tool_exec_status:
                for call in message.tool_calls:
                    call_result, call_status = asyncio.run(call_tool(call))
                    if call_status != "Success":
                        show_error(f"Error calling tool `{call.function.name}`: {call_status}")
                        LOG.error(f"Error calling tool `{call.function.name}`: {call_status}")
                    else:
                        with st.container(border=True):
                            tool_summary = [{"ID": call.id, "TOOL": call.function.name, "ARGUMENTS": call.function.arguments}]
                            st.write("###### Tool Call Summary")
                            st.dataframe(tool_summary, use_container_width=True, hide_index=True)
                            st.write("###### Tool Call Result")
                            st.write(f"**Result**: {call_result.content if call_result.content else ''}")
                            st.write(f"**Structured Result**: {call_result.structured_content if call_result.structured_content else ''}  :primary-badge[*This is part of the MCP protocol version 2025-06-18.*]")

                        messages.append({
                            "role": "assistant",
                            "tool_call_id": call.id,
                            "content": call_result.content[0].text
                        })

                tool_exec_status.update(label=f"{EXECUTE_ICON} Execute Selected Tools.", state="complete", expanded=False)

            with st.status(f"{LLM_ICON} Final LLM Response", expanded=True) as final_llm_status:
                try:
                    final_message = get_llm_tool_selection_response(
                        model=selected_model,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        messages=messages,
                        tools=aoai_tools,
                        tool_choice="none"
                    )

                    st.write("###### Final LLM Response")
                    st.markdown(final_message.content,)

                except Exception as e:
                    show_error(f"Error getting final LLM response: {e}")
                    LOG.error(f"Error getting final LLM response: {e}")
                    final_llm_status.update(label=f":red[Error getting final LLM response: {e}]", state="error", expanded=True)

        else:
            show_error("No tools were selected by the LLM.")



