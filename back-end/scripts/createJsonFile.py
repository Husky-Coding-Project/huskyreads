""" This program creates a clean JSON file from dirty book data.

This program uses regex and OS commands to edit and manipulate the
original dirty book data
"""

import re
import os
import json
import yaml

CURRENT_DIR = os.getcwd()
BACKEND_ROOT = os.path.abspath(CURRENT_DIR + '/..')
PROCESSED_DATA_PATH = os.path.join(BACKEND_ROOT, 'data', 'processed')

def text_cleaner(current_line: str) -> str:
    """ Removes the current line into cleaned JSON text

        Args:
            current_line:
                The current line being looked at

        Returns:
            The processed and correctly formatted JSON line
    """
    regex_result = re.search("{.*", current_line)
    return regex_result[0]

def parse_text_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()

    return file_lines

def append_multiple_lines(lines_to_append: str, output_path=os.path.join(PROCESSED_DATA_PATH,
                          "sample_output.json")):
    """
    Creates and Appends the clean book data into a JSON file

    If the file has not been created, it will create the file.
    Appends each book as its own separate line

    Args:
        lines_to_append:
            A list of all books within the dirty data

        output_path:
            The location of where the processed output will go.
            Defaults to a text file in data/processed called processed_output.
    """

    book_data = list(dict())
    for line in lines_to_append:
        cleaned_line = text_cleaner(line)
        book_data.append(cleaned_line)

    final_result = {'data': list(dict())}
    with open(output_path, 'a+', encoding='utf-8') as f_out:
        for i in range(len(book_data)):
            final_result['data'].append(json.loads(book_data[i]))

        f_out.write(json.dumps(final_result, indent = 4, sort_keys = False))


def main():
    for filename in os.listdir("../data/raw"):
        file_lines = parse_text_file("../data/raw/" + filename)
        output_file = filename.split(".")[0] + ".json"
        append_multiple_lines(file_lines, "../data/processed/" + output_file)

if __name__ == '__main__':
    main()

