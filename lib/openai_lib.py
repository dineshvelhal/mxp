import json
import logging
import os

from openai import OpenAI

LOG = logging.getLogger(__name__)

OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_openai_client():
    """
    Get OpenAI client for making requests.
    :return: OpenAI client
    """
    LOG.info("Initializing OpenAI client...")
    if OPEN_AI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    # Initialize the OpenAI client with the API key
    return OpenAI(api_key=OPEN_AI_API_KEY, )

def get_openai_response(prompt: str) -> str:
    """
    Get OpenAI response for a given prompt.
    :param prompt:
    :return: OpenAI response
    """
    LOG.info(f"Getting OpenAI response for prompt: {prompt}")
    if OPEN_AI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100,
    )

    ret_val = response.choices[0].message.content.strip()
    LOG.info(f"OpenAI response: {ret_val}")
    return ret_val


def get_tool_intent_check(tool_name: str, tool_description: str) -> str:
    """
    Check if the tool name and description are aligned with the intent.
    :param tool_name:
    :param tool_description:
    :return: intent check result as str
    """

    LOG.info(f"Checking tool intent for name: {tool_name} and description: {tool_description}")

    input_val = f"""
----------------------------------------------    
MCP Tool Name: {tool_name}

MCP Tool Description: {tool_description}
----------------------------------------------    
    """

    prompt = f"""
You are an AI assistant. Your task is to determine if the tool name and description are aligned with each other.
Please answer with "✅" or "❌" only.

1) Check if the tool name describes some intent or action.
2) Check if the tool description describes the tool's purpose and functionality in accordance with the tool name.

respond with one word only, either "✅" or "❌". No other text is needed.

{input_val}
"""
    response = get_openai_response(prompt)
    if response == "✅":
        LOG.info("Tool intent check passed.")
        return response
    else:
        LOG.warning("Tool intent check failed.")
        return response

def get_tool_input_check(tool_description, tool_input_schema) -> str:
    """
    Check if the description provides extra details about the tool input schema (E.g. description of the input arugments of the tool)
    :param tool_description:
    :param tool_input_schema:
    :return: input check result as string
    """
    LOG.info(f"Checking tool input for description: {tool_description} and input schema: {tool_input_schema}")



    input_val = f"""
----------------------------------------------
MCP Tool Description: {tool_description}

MCP Tool Input Schema: {tool_input_schema}
----------------------------------------------
    """

    prompt = f"""
You are an AI assistant. Your task is to determine if the tool description provides extra details about the tool input schema.
Please answer with "✅" or "❌" only.
1) Check if the tool description describes the input parameters (defined as properties in the input schema), 
their value ranges or anything else that tells more about the input parameters.
2) Answer "✅" only if some details is provided for all parameters involved. Otherwise answer "❌".

{input_val}
"""
    response = get_openai_response(prompt)
    if response == "✅":
        LOG.info("Tool input check passed.")
        return response
    else:
        LOG.warning("Tool input check failed.")
        return response


def get_tool_ret_val_check(tool_description) -> str:
    """
    Check if the description provides extra details about the tool return value (E.g. description of the output of the tool)
    :param tool_description:
    :return: return value check result as string
    """
    LOG.info(f"Checking tool return value for description: {tool_description}")

    input_val = f"""
----------------------------------------------
MCP Tool Description: {tool_description}
    
----------------------------------------------
    """

    prompt = f"""
You are an AI assistant. Your task is to determine if the tool description provides extra details about the tool return value.
Please answer with "✅" or "❌" only.
1) Check if the tool description describes the return value of the tool.
2) Answer "✅" only if some details is provided for the return value. Otherwise answer "❌".   
    
{input_val}
"""
    response = get_openai_response(prompt)
    if response == "✅":
        LOG.info("Tool return value check passed.")
        return response
    else:
        LOG.warning("Tool return value check failed.")
        return response


def get_tool_err_ret_val_check(tool_description) -> str:
    """
    Check if the description provides extra details about the tool error return value
    (E.g. description of the output of the tool in case of error)

    :param tool_description:
    :return: error return value check result as string
    """
    LOG.info(f"Checking tool error return value for description: {tool_description}")

    input_val = f"""
----------------------------------------------

MCP Tool Description: {tool_description}
----------------------------------------------
    """

    prompt = f"""   
You are an AI assistant. Your task is to determine if the tool description provides extra details various error responses
Please answer with "✅" or "❌" only.
1) Check if the tool description describes at least one error return value of the tool.
2) Answer "✅" only if some details is provided for the error return value. Otherwise answer "❌".
{input_val}
"""
    response = get_openai_response(prompt)
    if response == "✅":
        LOG.info("Tool error return value check passed.")
        return response
    else:
        LOG.warning("Tool error return value check failed.")
        return response


def get_annotations_check(tool_model_json: str) -> str:
    """
    Check if the tool model JSON contains annotations.
    :param tool_model_json:
    :return: "FULL", or "PARTIAL" or "NIL" based on the completeness of the annotations
    """
    LOG.info(f"Checking tool annotations for model JSON: {tool_model_json}")

    # convert tool_model_json to dict
    try:
        model_json_dict = json.loads(tool_model_json)

        annotations = model_json_dict.get("annotations", {})

        non_none_count = 0
        if annotations:
            # Check if all annotations are present and Not None
            for annotation in annotations:
                if annotations[annotation] is not None:
                    non_none_count += 1

            if non_none_count == len(annotations):
                LOG.info("Tool annotations check passed.")
                return "FULL"
            elif non_none_count > 0:
                LOG.info("Tool annotations check partially passed.")
                return "PARTIAL"
            else:
                LOG.warning("Tool annotations check failed.")
                return "NIL"
        else:
            return "NIL"
    except Exception as e:
        LOG.error(f"Failed to decode JSON: {e}")
        return "NIL"


def get_positive_test_cases(tool_name: str, tool_description: str, tool_input_schema: dict)-> str:
    """
    Fetch positive test cases for the given tool.
    :param tool_name:
    :param tool_description:
    :param tool_input_schema:
    :return:
    """
    LOG.info(f"Fetching positive test cases for tool: {tool_name}")

    input_val = f"""
    ----------------------------------------------
    MCP Tool Description: {tool_description}

    MCP Tool Input Schema: {tool_input_schema}
    ----------------------------------------------
        """

    prompt = f"""
    For the provided tool description and the Input Schema, generate a list of positive test cases that can be used to test the tool.
    Generate at the max 3 test cases.
    
    Output must be in the tabular format with tool parameters as columns followed by expected output as last column

    {input_val}
    """
    return get_openai_response(prompt)

