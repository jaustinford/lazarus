"""
Manage JSON data files used in
persisting application execution.
"""

import os
import json
import random
import string

import logs

def generate_id(string_length: int=40):
    """
    Create a random string given
    'string_length'.
    """

    random_string = ""

    for _ in range(string_length):
        random_string += random.choice(
            string.ascii_lowercase + \
            string.ascii_uppercase
        )

    return random_string

def create_json(file_path: str):
    """
    Create the JSON data file if
    missing.
    """

    file_name = os.path.basename(file_path).split('.')[-2]

    if not os.path.isfile(file_path):
        logs.GENERAL_LOGGER.info("Creating %s", file_name + " file : " + file_path)
        with open(file_path, "w", encoding="utf-8") as file_opened:
            file_opened.write(
                json.dumps(
                    {
                        file_name: []
                    },
                    indent=2
                )
            )

def read_json(file_path: str):
    """
    Open JSON data file and create as
    a JSON object.
    """

    file_name = os.path.basename(file_path).split('.')[-2]

    with open(file_path, "r", encoding="utf-8") as file_opened:
        file_read = file_opened.read()
        file_list = json.loads(file_read)[file_name]

    return file_list

def write_json(file_path: str, file_list: list):
    """
    Write the JSON object to the
    JSON data file.
    """

    file_name = os.path.basename(file_path).split('.')[-2]

    with open(file_path, "w", encoding="utf-8") as file_opened:
        file_opened.write(
            json.dumps(
                {
                    file_name: file_list
                },
                indent=2
            )
        )
