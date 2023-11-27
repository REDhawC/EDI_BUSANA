import nbformat


def extract_markdown_from_ipynb(file_path):
    """
    Extracts all Markdown content from a Jupyter Notebook file.

    :param file_path: Path to the Jupyter Notebook file.
    :return: List of strings, each representing a Markdown cell.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        notebook = nbformat.read(file, as_version=4)

    markdown_cells = [
        cell["source"] for cell in notebook["cells"] if cell["cell_type"] == "markdown"
    ]
    return markdown_cells


# Usage
file_path = "./PAMD_FINAL!.ipynb"  # Replace with the path to your notebook
markdown_content = extract_markdown_from_ipynb(file_path)

# Printing the extracted Markdown content
for index, markdown in enumerate(markdown_content):
    print(f"\n{markdown}\n")
