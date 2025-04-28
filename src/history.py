"""
Manage executed cycle tasks in
a separate .history.json.
"""

import os
import json
import datetime
import logs

logger = logs.logging.getLogger(__name__)

def create_json(history_file: str):
    """
    Create the .history.json file
    if missing.
    """

    if not os.path.isfile(history_file):
        logger.info("Creating history file : %s", history_file)
        with open(history_file, "w", encoding="utf-8") as history_opened:
            history_opened.write(
                json.dumps(
                    {
                        "history": []
                    },
                    indent=2
                )
            )

def read_json(history_file: str):
    """
    Open history.json file and assign as
    a JSON object.
    """

    with open(history_file, "r", encoding="utf-8") as history_opened:
        history_read = history_opened.read()
        history_json = json.loads(history_read)["history"]

    return history_json

def update_json(history_file: str, cycle_mode: str, cycle_object: object):
    """
    Open .history.json file, append new
    item and write out to file.
    """

    cycle_id = cycle_object["id"]

    history_json = read_json(history_file)

    history_json.append(
        {
            "cycle_id": cycle_id,
            "mode": cycle_mode,
            "added": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )

    with open(history_file, "w", encoding="utf-8") as history_opened:
        history_opened.write(
            json.dumps(
                {
                    "history": history_json
                },
                indent=2
            )
        )

def item_exists(history_file: str, cycle_mode: str, cycle_object: object):
    """
    Return boolean value for the
    existance of .history.json file
    item.
    """

    cycle_id = cycle_object["id"]

    history_json = read_json(history_file)

    item_found = False

    for history_item in history_json:
        if history_item["cycle_id"] == cycle_id:
            if history_item["mode"] == cycle_mode:
                item_found = True
                break

    return item_found
