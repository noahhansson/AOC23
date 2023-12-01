import os


def read_input(file_name: str) -> list[str]:
    """Function for navigating to data folder and reading input.

    Args:
        file_name (str): File name to read.

    Returns:
        list[str]: Returns the input where each row is a list element
    """

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    input_file = os.path.join(os.getcwd(), "..", "input", f"{file_name}")
    with open(input_file, 'r') as file:
        contents = [val.strip() for val in file.readlines()]

    return contents
