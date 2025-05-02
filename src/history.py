"""
Manage executed cycle tasks in
a persisted .history.json data file.
"""

import datetime

import constants
import datafile

def add_json(cycle_mode: str, cycle_object: object):
    """
    Open .history.json file, append new
    item and write out to file.
    """

    cycle_id   = cycle_object["id"]
    cycle_type = cycle_object["type"]

    history_json = datafile.read_json(constants.HISTORY_PATH)

    history_json.append(
        {
            "id": cycle_id,
            "type": cycle_type,
            "mode": cycle_mode,
            "added": datetime.datetime.now().strftime(constants.TIME_FORMAT_TIMESTAMP)
        }
    )

    datafile.write_json(
        constants.HISTORY_PATH,
        history_json
    )

def item_exists(cycle_mode: str, cycle_object: object):
    """
    Return boolean value for the
    existance of .history.json file
    item.
    """

    cycle_id = cycle_object["id"]

    history_json = datafile.read_json(constants.HISTORY_PATH)

    item_found = False

    for history_item in history_json:
        if history_item["cycle_id"] == cycle_id:
            if history_item["mode"] == cycle_mode:
                item_found = True
                break

    return item_found
