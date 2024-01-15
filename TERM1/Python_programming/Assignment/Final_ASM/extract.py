import nbformat


def extract_code_from_ipynb(notebook_path, output_path):
    # Load the notebook
    with open(notebook_path, "r", encoding="utf-8") as file:
        notebook = nbformat.read(file, as_version=4)

    # Extract code cells
    code_cells = [cell.source for cell in notebook.cells if cell.cell_type == "code"]

    # Write to a Python file
    with open(output_path, "w", encoding="utf-8") as output_file:
        for code in code_cells:
            output_file.write(code + "\n\n")


# Example usage
notebook_path = "./test2.ipynb"  # Replace with the path to your .ipynb file
output_path = "output2_script.py"  # The path for the output .py file

extract_code_from_ipynb(notebook_path, output_path)
