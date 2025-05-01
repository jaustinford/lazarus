"""
Manage executed cycle tasks in
a persisted .history.json data file.
"""

import datetime
import datafile

def add_json(history_path: str, cycle_mode: str, cycle_object: object):
    """
    Open .history.json file, append new
    item and write out to file.
    """

    cycle_id = cycle_object["id"]

    history_json = datafile.read_json(history_path)

    history_json.append(
        {
            "cycle_id": cycle_id,
            "mode": cycle_mode,
            "added": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    )

    datafile.write_json(
        history_path,
        history_json
    )

def item_exists(history_path: str, cycle_mode: str, cycle_object: object):
    """
    Return boolean value for the
    existance of .history.json file
    item.
    """

    cycle_id = cycle_object["id"]

    history_json = datafile.read_json(history_path)

    item_found = False

    for history_item in history_json:
        if history_item["cycle_id"] == cycle_id:
            if history_item["mode"] == cycle_mode:
                item_found = True
                break

    return item_found
