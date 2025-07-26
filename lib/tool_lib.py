import json
import logging
import pandas as pd

LOG = logging.getLogger(__name__)

def get_input_schema(tool: dict) -> (pd.DataFrame, str):
    """
        Get the input schema of a tool as a list of rows.
        :param tool: Tool dictionary containing the input schema
        :return: Input schema as a dictionary
    """
    result = "OK"
    LOG.info(f"Getting input schema for tool: {tool.get("NAME", "Unknown Tool")}")
    params_list = []
    model = tool.get("MODEL_JSON", "{}")
    # Convert JSON string to json object
    model_json = json.loads(model)

    input_schema = model_json.get("inputSchema", {})
    required_params = input_schema.get("required", [])
    for key, value in input_schema.get("properties", {}).items():
        row = {"PARAMETER": key, "TITLE": value.get("title", "")}
        if key in required_params:
            row["REQUIRED"] = True
        else:
            row["REQUIRED"] = False

        for k, v in value.items():
            if k != "title":
                row[k.upper()] = v

        if "DESCRIPTION" not in row:
            row["DESCRIPTION"] = None
            result = "MISSING/INCOMPLETE"

        params_list.append(row)

    # Check if params_list is empty
    if not params_list:
        LOG.warning("No parameters found in the input schema.")
        raise ValueError("No parameters found in the input schema.")
    else:
        df = pd.DataFrame(params_list)
        df1 = (df.style
               .map(style_parameter_column, subset=["PARAMETER"])
               .map(style_highlight_red_if_none, subset=["DESCRIPTION"]))

    return df1, result


def get_output_schema(tool: dict) -> pd.DataFrame:
    """
        Get the output schema of a tool as a list of rows.
        :param tool: Tool dictionary containing the output schema
        :return: Output schema as a dictionary
    """
    LOG.info(f"Getting output schema for tool: {tool.get("NAME", "Unknown Tool")}")
    params_list = []
    model = tool.get("MODEL_JSON", "{}")
    # Convert JSON string to json object
    model_json = json.loads(model)

    output_schema = model_json.get("outputSchema", {})
    # required_params = input_schema.get("required", [])
    if not output_schema:
        LOG.warning("No output schema found in the tool model.")
        raise ValueError("No output schema found in the tool model.")

    for key, value in output_schema.get("properties", {}).items():
        row = {"PARAMETER": key, "TITLE": value.get("title", "")}

        for k, v in value.items():
            if k != "title":
                row[k.upper()] = v

        # if "description" not in row:
        #     row["DESCRIPTION"] = None

        params_list.append(row)

    # Check if params_list is empty
    if not params_list:
        LOG.warning("No parameters found in the output schema.")
        raise ValueError("No parameters found in the output schema.")
    else:
        df = pd.DataFrame(params_list)

    return df


def style_parameter_column(val):
    return "color: blue;"

def style_highlight_red_if_none(val):
    if val is None or (isinstance(val, str) and val.strip() == ""):
        return "color: red; background-color: #FFCCCC;"
    else:
        return ""


def style_tool_name_column(val):
    return "font-weight: bold"


def get_annotations(tool: dict) -> (pd.DataFrame, str):
    """
        Get the annotations of a tool as a list of rows.
        :param tool: Tool dictionary containing the annotations
        :return: Annotations as a DataFrame
    """
    result = "OK"
    LOG.info(f"Getting annotations for tool: {tool.get("NAME", "Unknown Tool")}")

    model = tool.get("MODEL_JSON", "{}")
    # Convert JSON string to json object
    model_json = json.loads(model)

    annotations = model_json.get("annotations", {})
    # required_params = input_schema.get("required", [])
    if not annotations:
        LOG.warning("No annotations found in the tool model.")
        raise ValueError("No annotations found in the tool model.")


    annotations_dict = [{
        "TITLE": annotations.get("title", None),
        "READ ONLY HINT": annotations.get("readOnlyHint", None),
        "DESTRUCTIVE HINT": annotations.get("destructiveHint", None),
        "IDEMPOTENT HINT": annotations.get("idempotentHint", None),
        "OPEN WORLD HINT": annotations.get("openWorldHint", None),
    }]

    for k, v in annotations_dict[0].items():
        if v is None:
            result = "MISSING/INCOMPLETE"
            break

    df = pd.DataFrame(annotations_dict)
    df1 = (df.style.map(style_highlight_red_if_none))

    return df1, result


def make_analysis_colorful(df: pd.DataFrame):
    """
    Apply styles to the DataFrame to make it colorful based on the values.
    :param df: DataFrame to style
    :return: Styled DataFrame
    """
    return (df.style
            .map(lambda x: 'background-color: #FFCCCC; color: black;' if x in ("MISSING/INCOMPLETE", "MISSING") else '', subset=["TOOL DESCRIPTION", "INPUT SCHEMA", "OUTPUT SCHEMA", "ANNOTATIONS"])
            .map(lambda x: 'background-color: #CCFFCC; color: black;' if x == "OK" else '', subset=["TOOL DESCRIPTION", "INPUT SCHEMA", "OUTPUT SCHEMA", "ANNOTATIONS"])
            .map(style_tool_name_column, subset=["TOOL NAME"]))