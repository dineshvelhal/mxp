# md/md_lib.py

"""
MarkdownCreator: Utility class for progressive creation of Markdown documents.
Provides methods to add headers, lists, tables, and save the document.
"""

import logging
from typing import List
import os
import datetime

LOG = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

class MarkdownCreator:
    """
    Class to progressively build a Markdown document and save it to a file.
    """

    def __init__(self, filename: str):
        """
        Initialize MarkdownCreator with the target filename.

        Parameters:
            filename (str): The name of the file to save the markdown document.
        """
        LOG.info("Initializing MarkdownCreator")
        self.filename = filename
        self._content = []


    def _return_header(self, header_text: str, level: int) -> str:
        """
        Add a header of specified level.

        Parameters:
            header_text (str): The text of the header.
            level (int): The level of the header (1-6).

        Returns:
            str: The markdown header string.
        """
        LOG.info(f"Adding h{level} header")
        header = f"{'#' * level} {header_text}\n\n"
        self._content.append(header)
        return header

    def h1(self, text: str) -> str:
        """
        Add a level 1 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 1)

    def h2(self, text: str) -> str:
        """
        Add a level 2 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 2)

    def h3(self, text: str) -> str:
        """
        Add a level 3 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 3)

    def h4(self, text: str) -> str:
        """
        Add a level 4 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 4)

    def h5(self, text: str) -> str:
        """
        Add a level 5 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 5)

    def h6(self, text: str) -> str:
        """
        Add a level 6 header.

        Parameters:
            text (str): The header text.

        Returns:
            str: The markdown header string.
        """
        return self._return_header(text, 6)


    def list(self, items: List[str]) -> str:
        """
        Add a bulleted list.

        Parameters:
            items (List[str]): List of items to include in the bulleted list.

        Returns:
            str: The markdown list string.
        """
        LOG.info("Adding bulleted list")
        if not items:
            LOG.warning("Empty list provided to add_list")
        list_md = "\n".join([f"- {item}" for item in items]) + "\n"
        list_md = list_md + "\n"  # Ensure a newline after the list
        self._content.append(list_md)
        return list_md


    def numbered_list(self, items: List[str]) -> str:
        """
        Add a numbered list.

        Parameters:
            items (List[str]): List of items to include in the numbered list.

        Returns:
            str: The markdown numbered list string.
        """
        LOG.info("Adding numbered list")
        if not items:
            LOG.warning("Empty list provided to add_numbered_list")
        list_md = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)]) + "\n"
        list_md = list_md + "\n"
        self._content.append(list_md)
        return list_md


    def table_from_list_of_list(self, table: List[List[str]]) -> str:
        """
        Add a markdown table from a list of lists or pandas DataFrame.

        Parameters:
            table List[List[str]]: Table data as a list of lists.

        Returns:
            str: The markdown table string.
        """
        LOG.info("Adding table")
        if isinstance(table, list) and table and isinstance(table[0], list):
            LOG.info("Table input is a list of lists")
            headers = table[0]
            rows = table[1:]
        else:
            LOG.warning("Invalid table input")
            raise ValueError("Table must be a list of lists or a pandas DataFrame")

        header_md = "| " + " | ".join(headers) + " |\n"
        separator_md = "| " + " | ".join(["---"] * len(headers)) + " |\n"
        rows_md = ""
        for row in rows:
            rows_md += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        table_md = header_md + separator_md + rows_md
        table_md += "\n"
        self._content.append(table_md)
        return table_md

    def table_from_list_of_dict(self, table: List[dict]) -> str:
        """
        Add a markdown table from a list of dictionaries.

        Parameters:
            table (List[dict]): Table data as a list of dictionaries.

        Returns:
            str: The markdown table string.
        """
        LOG.info("Get unique set of all properties from all items in the table")
        if not table:
            LOG.warning("Empty table provided to add_table_from_list_of_dict")
            return ""
        headers = []
        for item in table:
            for key in item.keys():
                headers.append(key)
            # headers.append(item.keys())
            LOG.debug(f"Current headers: {headers}")

        md_table_header = "| " + " | ".join(headers) + " |\n"
        # Create a separator row
        separator_md = "| " + " | ".join(["---"] * len(headers)) + " |\n"
        rows_md = ""

        for item in table:
            row = "| " + " | ".join(str(item.get(header, "")) for header in headers) + " |\n"
            rows_md += row

        table_md = md_table_header + separator_md + rows_md
        table_md += "\n"  # Ensure a newline after the table
        self._content.append(table_md)
        LOG.info("Table added successfully")
        return table_md

    def paragraph(self, text: str) -> str:
        """
        Add a paragraph.

        Parameters:
            text (str): The paragraph text.

        Returns:
            str: The markdown paragraph string.
        """
        LOG.info("Adding paragraph")
        paragraph = f"{text}\n\n"

        self._content.append(paragraph)
        return paragraph

    def code(self, code: str, language: str = "text") -> str:
        """
        Add a code block.

        Parameters:
            code (str): The code to include in the block.
            language (str): The programming language for syntax highlighting (default is "text").

        Returns:
            str: The markdown code block string.
        """
        LOG.info("Adding code block")
        code_block = f"```{language}\n{code}\n```\n\n"
        self._content.append(code_block)
        return code_block

    def md_doc(self) -> str:
        """
        Get the current markdown document as a string.

        Returns:
            str: The complete markdown document.
        """
        LOG.info("Retrieving markdown document")
        return "".join(self._content)


    def save_to_file(self) -> None:
        """
        Save the markdown document to the file specified in the constructor.

        Returns:
            None
        """
        LOG.info("Saving markdown document to file")
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(self.md_doc())


def create_report_folder(base_dir: str = "reports", folder_name=None) -> str:
    """
    Create a report folder with the name as current timestamp in the format "YYYY-MM-DD_HH-MM-SS".
    """

    LOG.info(f"Creating report folder: {folder_name}")

    if not folder_name:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_folder = os.path.join(base_dir, timestamp)
    else:
        report_folder = os.path.join(base_dir, folder_name)

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)
        LOG.info(f"Report folder created: {report_folder}")
    else:
        LOG.warning(f"Report folder already exists: {report_folder}")

    return report_folder

def create_file(base_dir, str, file_name: str, file_contents: str) -> str:
    """
    Create a file with the specified name and contents in the given directory.

    Parameters:
        base_dir (str): The base directory where the file will be created.
        file_name (str): The name of the file to create.
        file_contents (str): The contents to write to the file.

    Returns:
        str: The full path of the created file.
    """
    LOG.info(f"Creating file: {file_name} in {base_dir}")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    file_path = os.path.join(base_dir, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_contents)

    LOG.info(f"File created: {file_path}")
    return file_path