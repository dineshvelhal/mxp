import collections
import logging
import os
import shutil
import yaml
from fastmcp import Client
from typing import Literal

from fastmcp.client import SSETransport, StreamableHttpTransport

from lib.common_lib import get_mcp_schema, get_report_config_dict
from lib.md_lib import create_report_folder, MarkdownCreator

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


class MCPServerDoc:
    """Class representing an MCP server for documentation purposes."""

    def __init__(self,
                 name:str,
                 transport_type: Literal['SSE', 'Streamable-HTTP'],
                 url: str,
                 version: str= None):
        """
        Initialize the MCPServer instance.
        :param name: Server name
        :param transport_type: Transport type of the MCP server (e.g., 'SSE', 'Streamable-HTTP')
        :param url: URL of the MCP server
        :param version: Version of the MCP server (optional)
        """
        LOG.info(f"Initializing MCPServerDoc: name={name}, transport_type={transport_type}, url={url}, version={version}")
        self.name = name
        self.transport_type = transport_type
        self.url = url
        self.version = version
        self.document_tool_type = "mkdocs"  # Default target for documentation generation
        self.output_directory = "docs"  # Default output directory for documentation
        self.tools = []
        self.resources = []
        self.resource_templates = []
        self.prompts = []
        self.loaded = False

        if transport_type == 'SSE':
            LOG.info(f"Using SSETransport for URL: {url}")
            transport = SSETransport(url)
            self.client = Client(transport=transport)
        elif transport_type == 'Streamable-HTTP':
            LOG.info(f"Using StreamableHttpTransport for URL: {url}")
            transport = StreamableHttpTransport(url)
            self.client = Client(transport=transport)
        else:
            LOG.error(f"Unknown transport_type: {transport_type}")
            raise ValueError(f"Unknown transport_type: {transport_type}")

        LOG.info("MCPServerDoc initialized successfully")

    def __str__(self):
        LOG.debug("Converting MCPServerDoc to string")
        return f"MCPServer(name={self.name}, transport_type={self.transport_type}, url={self.url}, version={self.version})"

    async def load_schema(self):
        """
        Load the server schema.

        :return: Tuple of (tools, resources, prompts) as lists
        """
        LOG.info("Loading server schema using get_mcp_schema")

        tools, resources, resource_templates, prompts = await get_mcp_schema(self.client)
        self.tools = tools
        self.resources = resources
        self.resource_templates = resource_templates
        self.prompts = prompts

        LOG.info("Server schema loaded successfully")
        self.loaded = True
        return tools, resources, resource_templates, prompts

    def set_document_tool_type(self, target: Literal["mkdocs", "mdutils"]):
        """
        Set the documentation target.
        :param target: Either "mkdocs" or "mdutils"
        """
        LOG.debug(f"Setting document target to: {target}")
        if target not in ("mkdocs", "mdutils"):
            LOG.error(f"Invalid document target: {target}")
            raise ValueError("Invalid document target. Allowed values are 'mkdocs' or 'mdutils'.")
        self.document_tool_type = target
        LOG.info(f"Document target set to: {self.document_tool_type}")

    def set_output_directory(self, directory: str):
        """
        Set the output directory for documentation.
        :param directory: Path to the output directory
        """
        LOG.debug(f"Setting output directory to: {directory}")
        self.output_directory = directory
        LOG.info(f"Output directory set to: {self.output_directory}")

    def generate_documentation(self) -> str:
        """

        :return: Path of the generated documentation folder
        """
        if self.loaded:
            LOG.info("Generating documentation for MCP server")
            if self.document_tool_type == "mkdocs":
                LOG.info("Generating documentation using MkDocs")
                # Create the output directory if it doesn't exist
                report_folder = create_report_folder()

                docs_folder = create_report_folder(report_folder, "docs")
                tools_folder = create_report_folder(docs_folder, "tools")
                resources_folder = create_report_folder(docs_folder, "resources")
                resource_templates_folder = create_report_folder(docs_folder, "resource_templates")
                prompts_folder = create_report_folder(docs_folder, "prompts")

                report_config_file = f"{report_folder}/mkdocs.yml"
                report_config_dict = get_report_config_dict(self)
                with open(report_config_file, "w", encoding="utf-8") as f:
                    yaml.dump(report_config_dict, f, sort_keys=False)

                # Add index.md in the docs folder
                index_file = os.path.join(docs_folder, "index.md")
                mc = MarkdownCreator(index_file)
                mc.h1(self.name)
                mc.table_from_list_of_list([
                    ["Transport Type", "URL", "Version"],
                    [self.transport_type, self.url, self.version if self.version else "N/A"]
                ])
                mc.save_to_file()

                # Copy assets folder to docs folder
                assets_folder = os.path.join(os.path.dirname(__file__), "assets")
                if os.path.exists(assets_folder):
                    destination_folder = os.path.join(docs_folder, "assets")
                    shutil.copytree(assets_folder, destination_folder)


                # Add tools documentation
                for tool in self.tools:
                    tool_file = os.path.join(tools_folder, f"{tool['NAME']}.md")
                    mc = MarkdownCreator(tool_file)
                    mc.h1(f"🛠️ {tool['NAME']}")
                    # mc.paragraph(f"**Title:** {tool.get('TITLE', 'N/A')}")
                    mc.paragraph("**Tool Description:**")
                    mc.code(tool["DESCRIPTION"],)
                    # title_description = [
                    #     ["Title", "Description"],
                    #     [tool.get("TITLE", "N/A"), tool.get("DESCRIPTION", "N/A")]
                    # ]
                    # mc.table_from_list_of_list(title_description)
                    mc.h2("📥 Input Parameters")
                    input_params = tool.get("INPUT_PARAMS", [])
                    # mc.table_from_list_of_dict(input_params)
                    for input_param in input_params:
                        mc.h3(f"<kbd>{input_param.get("PARAMETER", "N/A")}</kbd>")
                        # mc.paragraph(f"**Description:**")
                        mc.code(input_param.get("DESCRIPTION", "N/A"))
                        # get input_param by excluding NAME, TITLE, DESCRIPTION
                        input_param_details = {k: v for k, v in input_param.items() if k not in ["PARAMETER", "TITLE", "DESCRIPTION"]}

                        p1 = {k: v for k, v in input_param_details.items() if k == 'REQUIRED'}
                        p2 = {k: v for k, v in input_param_details.items() if k == 'TYPE'}
                        p3 = {k: v for k, v in input_param_details.items() if k not in ['REQUIRED', 'TYPE']}

                        p4 = collections.OrderedDict()
                        p4.update(p1)
                        p4.update(p2)
                        p4.update(p3)

                        p5 = collections.OrderedDict()
                        for k, v in p4.items():
                            if k == 'ENUM' and isinstance(v, list):
                                val = ""
                                for item in v:
                                    val = val + f"<kbd>{item}</kbd> "
                                p5[k] = val.strip()
                            else:
                                p5[k] = v

                        mc.table_from_list_of_dict([p5])
                    mc.h2("📤 Output Schema")
                    output_params = tool.get("OUTPUT_PARAMS", [])
                    mc.table_from_list_of_dict(output_params)
                    mc.h2("🏷️ Annotations")
                    annotations = tool.get("ANNOTATIONS", {})
                    mc.table_from_list_of_dict([annotations])
                    mc.save_to_file()

                # Add resources documentation
                for resource in self.resources:
                    resource_file = os.path.join(resources_folder, f"{resource['NAME']}.md")
                    mc = MarkdownCreator(resource_file)
                    mc.h1(f"📦 {resource['NAME']}")
                    mc.paragraph(f"**Resource Description:**")
                    mc.code(resource.get('DESCRIPTION', 'N/A'))

                    mc.paragraph("**Resource Parameters**")
                    other_params = {k: v for k, v in resource.items() if k not in ['NAME', 'DESCRIPTION', 'TITLE']}
                    mc.table_from_list_of_dict([other_params])

                    mc.save_to_file()

                # Add resource templates documentation
                for template in self.resource_templates:
                    template_file = os.path.join(resource_templates_folder, f"{template['NAME']}.md")
                    mc = MarkdownCreator(template_file)
                    mc.h1(f"🧩 {template['NAME']}")
                    mc.paragraph(f"**Template Description:**")
                    mc.code(template.get('DESCRIPTION', 'N/A'))

                    mc.paragraph("**Template Parameters**")
                    other_template_params = {k: v for k, v in template.items() if k not in ['NAME', 'DESCRIPTION', 'TITLE']}
                    mc.table_from_list_of_dict([other_template_params])

                    mc.save_to_file()

                # Add prompts documentation
                for prompt in self.prompts:
                    prompt_file = os.path.join(prompts_folder, f"{prompt['NAME']}.md")
                    mc = MarkdownCreator(prompt_file)
                    mc.h1(f"💬 {prompt['NAME']}")
                    mc.paragraph(f"**Prompt Description:**")
                    mc.code(prompt.get('DESCRIPTION', 'N/A'))

                    mc.paragraph("**Prompt Parameters**")
                    other_prompt_params = {k: v for k, v in prompt.items() if k not in ['NAME', 'DESCRIPTION', 'TITLE']}
                    mc.table_from_list_of_dict(other_prompt_params["ARGUMENTS"])

                    mc.save_to_file()

                LOG.info(f"Documentation generated successfully in {report_folder}")
                return report_folder
            elif self.document_tool_type == "mdutils":
                raise NotImplementedError("MDUtils documentation generation is not implemented yet")
        else:
            raise Exception("Load schema before generating documentation")