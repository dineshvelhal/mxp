import json
import logging
import os

import fastmcp
from mcp import McpError

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


def get_tool_schema(tools) -> list:
    """
    Extract and format the schema for a list of tools.

    :param tools: List of tool objects
    :return: List of tool schema dictionaries
    """
    LOG.info("Starting to extract tool schemas")
    tool_list = []
    for tool in tools:
        LOG.info(f"Processing tool: {tool.name}")
        model = tool.model_dump_json()
        # Convert JSON string to json object
        model_json = json.loads(model)

        tool_row = {
            "NAME": tool.name,
            "TITLE": tool.title,
            "DESCRIPTION": tool.description,
        }

        input_param_list = []
        input_schema = model_json.get("inputSchema", {})
        required_params = input_schema.get("required", [])
        LOG.info(f"Extracting input parameters for tool: {tool.name}")
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

            input_param_list.append(row)

        tool_row["INPUT_PARAMS"] = input_param_list

        output_params_list = []
        output_schema = model_json.get("outputSchema", {})
        if not output_schema:
            LOG.info(f"No output schema found for tool: {tool.name}")
            pass
        else:
            LOG.info(f"Extracting output parameters for tool: {tool.name}")
            for key, value in output_schema.get("properties", {}).items():
                row = {"PARAMETER": key, "TITLE": value.get("title", "")}

                for k, v in value.items():
                    if k != "title":
                        row[k.upper()] = v

                # if "description" not in row:
                #     row["DESCRIPTION"] = None

                output_params_list.append(row)

        tool_row["OUTPUT_PARAMS"] = output_params_list

        LOG.info(f"Extracting annotations for tool: {tool.name}")
        annotations = model_json.get("annotations", {})

        if annotations:
            annotations_dict = {
                "TITLE": annotations.get("title", ""),
                "READ ONLY HINT": "✅" if annotations["readOnlyHint"] == True else annotations["readOnlyHint"],
                "DESTRUCTIVE HINT": "✅" if annotations["destructiveHint"] == True else annotations["destructiveHint"],
                "IDEMPOTENT HINT": "✅" if annotations["idempotentHint"] == True else annotations["idempotentHint"],
                "OPEN WORLD HINT": "✅" if annotations["openWorldHint"] == True else annotations["openWorldHint"],
            }
        else:
            LOG.warning(f"No annotations found for tool: {tool.name}")
            annotations_dict = {
                "TITLE": "",
                "READ ONLY HINT": "",
                "DESTRUCTIVE HINT": "",
                "IDEMPOTENT HINT": "",
                "OPEN WORLD HINT": "",
            }

        tool_row["ANNOTATIONS"] = annotations_dict

        tool_list.append(tool_row)
        LOG.info(f"Finished processing tool: {tool.name}")

    LOG.info("Completed extraction of all tool schemas")
    return tool_list


def get_resource_schema(resources) -> list:
    """
    Extract and format the schema for a list of resources.

    :param resources: List of resource objects
    :return: List of resource schema dictionaries
    """
    LOG.info("Starting to extract resource schemas")
    resource_list = []
    for resource in resources:
        LOG.info(f"Processing resource: {resource.name}")
        model = resource.model_dump_json()
        # Convert JSON string to json object
        model_json = json.loads(model)

        resource_row = {
            "NAME": resource.name,
            "TITLE": resource.title,
            "DESCRIPTION": resource.description,
        }
        # loop over the model_json to extract properties
        LOG.info(f"Extracting properties for resource: {resource.name}")
        for key, value in model_json.items():
            if key not in resource_row.keys():
                resource_row[key.upper()] = value

        LOG.info(f"Resource Model JSON: {model_json}")

        # Assuming resources have similar structure as tools, adjust as necessary
        # Add more fields as needed based on the actual resource schema

        resource_list.append(resource_row)
        LOG.info(f"Finished processing resource: {resource.name}")

    LOG.info("Completed extraction of all resource schemas")
    return resource_list


def get_resource_template_schema(resource_templates) -> list:
    """
    Extract and format the schema for a list of resource templates.

    :param resource_templates: List of resource template objects
    :return: List of resource template schema dictionaries
    """
    LOG.info("Starting to extract resource template schemas")
    resource_template_list = []
    for template in resource_templates:
        LOG.info(f"Processing resource template: {template.name}")
        model = template.model_dump_json()
        # Convert JSON string to json object
        model_json = json.loads(model)

        template_row = {
            "NAME": template.name,
            "TITLE": template.title,
            "DESCRIPTION": template.description,
        }
        # loop over the model_json to extract properties
        LOG.info(f"Extracting properties for resource: {template.name}")
        for key, value in model_json.items():
            if key not in template_row.keys():
                template_row[key.upper()] = value

        LOG.info(f"Resource Template Model JSON: {model_json}")

        # Assuming templates have similar structure as tools, adjust as necessary
        # Add more fields as needed based on the actual resource template schema

        resource_template_list.append(template_row)
        LOG.info(f"Finished processing resource template: {template.name}")

    LOG.info("Completed extraction of all resource template schemas")
    return resource_template_list


def get_prompt_schema(prompts) -> list:
    """
    Extract and format the schema for a list of prompts.

    :param prompts: List of prompt objects
    :return: List of prompt schema dictionaries
    """
    LOG.info("Starting to extract prompt schemas")
    prompt_list = []
    for prompt in prompts:
        LOG.info(f"Processing prompt: {prompt.name}")
        model = prompt.model_dump_json()
        # Convert JSON string to json object
        model_json = json.loads(model)

        prompt_row = {
            "NAME": prompt.name,
            "TITLE": prompt.title,
            "DESCRIPTION": prompt.description,
        }
        LOG.info(f"Prompt Model JSON: {model_json}")

        if "arguments" in model_json:
            prompt_row["ARGUMENTS"] = model_json["arguments"]

        # Assuming prompts have similar structure as tools, adjust as necessary
        # Add more fields as needed based on the actual prompt schema

        prompt_list.append(prompt_row)
        LOG.info(f"Finished processing prompt: {prompt.name}")

    LOG.info("Completed extraction of all prompt schemas")
    return prompt_list


async def get_mcp_schema(client: fastmcp.Client):
    """
    Get the MCP server schema including tools, resources, and prompts.

    :param client: FastMCP client instance
    :return: Tuple containing lists of tools, resources, and prompts
    """
    LOG.info("Fetching MCP server schema")
    async with client:
        LOG.info("Connected to MCP client")

        LOG.info("Retrieving tools from MCP server")
        tools = await client.list_tools()
        LOG.info(f"Retrieved {len(tools)} tools from server")
        LOG.info("Extracting tool schemas from retrieved tools")
        tool_list = get_tool_schema(tools)

        LOG.info("Retrieving resources from MCP server")
        try:
            resources = await client.list_resources()
            LOG.info(f"Retrieved {len(resources)} resources from server")
            LOG.info("Extracting resource schemas from retrieved resources")
            resource_list = get_resource_schema(resources)
        except McpError as e:
            LOG.error(f"Resources not supported by MCP server: {e}")
            resource_list = []  # Placeholder for resources if not supported

        LOG.info("Retrieving resource templates from MCP server")
        try:
            resource_templates = await client.list_resource_templates()
            LOG.info(f"Retrieved {len(resource_templates)} resource templates from server")
            LOG.info("Extracting resource template schemas from retrieved resource templates")
            resource_template_list = get_resource_template_schema(
                resource_templates)  # Placeholder for resource templates
        except McpError as e:
            LOG.error(f"Resource templates not supported by MCP server: {e}")
            resource_template_list = []

        LOG.info("Retrieving prompts from MCP server")
        try:
            prompts = await client.list_prompts()
            LOG.info(f"Retrieved {len(prompts)} prompts from server")
            LOG.info("Extracting prompt schemas from retrieved prompts")
            prompt_list = get_prompt_schema(prompts)
        except McpError as e:
            LOG.error(f"Prompts not supported by MCP server: {e}")
            prompt_list = []

    LOG.info("Completed fetching and processing MCP server schema")
    return tool_list, resource_list, resource_template_list, prompt_list  # Returning empty lists for resources and prompts as placeholders


def get_report_config_dict(self):
    """
    Generate the configuration dictionary for MkDocs report.

    :param self: Instance of MCPServerDoc
    :return: Dictionary containing report configuration
    """
    LOG.info("Generating report configuration dictionary")
    config = {
        'site_name': self.name,
        'nav': [
            {'🏠 Home': 'index.md'},
            {'🛠️ Tools': [{tool['NAME']: f'tools/{tool["NAME"]}.md'} for tool in self.tools]},
            {'📦 Resources': [{resource['NAME']: f'resources/{resource["NAME"]}.md'} for resource in self.resources]},
            {'🧩 Resource Templates': [{template['NAME']: f'resource_templates/{template["NAME"]}.md'} for template in
                                      self.resource_templates]},
            {'💬 Prompts': [{prompt['NAME']: f'prompts/{prompt["NAME"]}.md'} for prompt in self.prompts]}
        ],
        'theme': {
            'name': 'material',
            'logo': 'assets/logo.png',
            'favicon': 'assets/icon.png',
            'features': ['header.autohide', 'navigation.footer'],
            "palette": [
                {
                    # Palette toggle for dark mode
                    "scheme": "slate",
                    "primary": "blue",
                    "accent": "green",
                    "toggle": {
                        "icon": "material/brightness-4",
                        "name": "Switch to light mode"
                    }
                },
                {
                    # Palette toggle for light mode
                    "scheme": "default",
                    "toggle": {
                        "icon": "material/brightness-7",
                        "name": "Switch to dark mode"
                    }
                }
            ]
        }
    }
    LOG.info("Report configuration dictionary generated successfully")
    return config
