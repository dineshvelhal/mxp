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


def get_llm_tool_selection_response(model: str,
                                    max_tokens: int,
                                    temperature: float,
                                    top_p: float,
                                    messages: list,
                                    tools: dict,
                                    tool_choice: str = "auto"):
    """
    Get LLM response for a given question.
    :param model:
    :param messages:
    :param tool_choice:
    :param tools:
    :param max_tokens:
    :param temperature:
    :param top_p:
    :return: LLM response
    """
    LOG.info(f"Getting LLM response for messages: {messages}")

    if OPEN_AI_API_KEY is None:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    client = get_openai_client()
    response = client.chat.completions.create(model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )

    message = response.choices[0].message

    return message


def get_test_cases(prompt: str) -> str:
    """
    Get test cases generated for a given prompt.
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
        max_tokens=800,
    )

    ret_val = response.choices[0].message.content.strip()
    LOG.info(f"OpenAI response: {ret_val}")
    return ret_val