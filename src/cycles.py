"""
Manage a persisted JSON data file
for tracking the various cycle
operations.
"""

import os
import datetime
import datafile
import logs
import history

logger = logs.logging.getLogger(__name__)

def remove_json(cycles_path: str, cycle_object: object):
    """
    Return a list of all cycles object, less
    the one provided in cycle_object.
    """

    removed_list = []

    cycle_id = cycle_object["id"]

    for file_object in datafile.read_json(cycles_path):
        if file_object["id"] != cycle_id:
            removed_list.append(file_object)

    return removed_list

def evaluate_object(cycle_mode: str, cycle_object: object):
    """
    Decide whether a cycle is
    conditional to run.
    """

    cycle_id   = cycle_object["id"]
    cycle_down = cycle_object["down"]
    cycle_up   = cycle_object["up"]

    should_run = False

    real_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    if cycle_mode == "down":
        mode_time = cycle_down

    elif cycle_mode == "up":
        mode_time = cycle_up

    if mode_time == "now":
        should_run = True

        logger.info(
            "Executing non-scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    elif mode_time == real_time:
        should_run = True

        logger.info(
            "Executing scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    return should_run

def process_mode(cycles_path: str, history_path: str, cycle_mode: str, cycle_object: object):
    """
    Execute tasks if a cycle has
    been determined to run.
    """

    should_run = evaluate_object(
        cycle_mode,
        cycle_object
    )

    if should_run:
        history.add_json(
            history_path,
            cycle_mode,
            cycle_object
        )

        os.environ["CYCLE_MODE"] = cycle_mode
        os.system("python /iac-configure/triggers/profile.py 2&> /dev/null")

        if cycle_mode == "up":
            removed_list = remove_json(
                cycles_path,
                cycle_object
            )

            datafile.write_json(
                cycles_path,
                removed_list
            )

def determine_mode(cycles_path: str, history_path: str, cycle_mode: str, cycle_object: object):
    """
    Sort through based on mode
    and process conditionals if
    active and .history.json item
    does not exist.
    """

    cycle_active = cycle_object["active"]

    if cycle_active:
        if not history.item_exists(history_path, cycle_mode, cycle_object):
            process_mode(
                cycles_path,
                history_path,
                cycle_mode,
                cycle_object
            )

def process_items(cycles_path: str, history_path: str):
    """
    Iterate over cycles.json and
    process down and up cycle jobs.
    """

    datafile.create_json(cycles_path)
    datafile.create_json(history_path)

    for cycle_object in datafile.read_json(cycles_path):
        determine_mode(
            cycles_path,
            history_path,
            "down",
            cycle_object
        )

        determine_mode(
            cycles_path,
            history_path,
            "up",
            cycle_object
        )
