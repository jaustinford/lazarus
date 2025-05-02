"""
Manage a persisted JSON data file
for tracking the various cycle
operations.
"""

import os
import datetime

import constants
import logs
import datafile
import history

def manage_lock(lock_mode: str, cycle_object: object):
    """
    Use a lock file to skip certain
    operations until lock file is
    removed.
    """

    if lock_mode == "add":
        logs.GENERAL_LOGGER.info("Creating cycles lock file : %s", constants.CYCLES_LOCK_PATH)
        with open(constants.CYCLES_LOCK_PATH, "w", encoding="utf-8") as cycle_lock_opened:
            cycle_lock_opened.write(cycle_object["id"])

    elif lock_mode == "remove":
        logs.GENERAL_LOGGER.info("Removing cycles lock file : %s", constants.CYCLES_LOCK_PATH)
        os.remove(constants.CYCLES_LOCK_PATH)

def remove_json(cycle_object: object):
    """
    Return a list of all cycles object, less
    the one provided in cycle_object.
    """

    removed_list = []

    cycle_id = cycle_object["id"]

    for file_object in datafile.read_json(constants.CYCLES_PATH):
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

    real_time = datetime.datetime.now().strftime(constants.TIMESTAMP_FORMAT)

    if cycle_mode == "down":
        mode_time = cycle_down

    elif cycle_mode == "up":
        mode_time = cycle_up

    if mode_time == "now":
        should_run = True

        logs.GENERAL_LOGGER.info(
            "Executing non-scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    elif mode_time == real_time:
        should_run = True

        logs.GENERAL_LOGGER.info(
            "Executing scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    return should_run

def process_mode(cycle_mode: str, cycle_object: object):
    """
    Execute tasks if a cycle has
    been determined to run.
    """

    should_run = evaluate_object(
        cycle_mode,
        cycle_object
    )

    if should_run:
        if cycle_mode == "down":
            manage_lock(
                "add",
                cycle_object
            )

        history.add_json(
            cycle_mode,
            cycle_object
        )

        os.environ["CYCLE_MODE"] = cycle_mode
        os.system("python /iac-configure/triggers/profile.py > /dev/null 2>&1")

        if cycle_mode == "up":
            datafile.write_json(
                constants.CYCLES_PATH,
                remove_json(cycle_object)
            )

            manage_lock(
                "remove",
                cycle_object
            )

def determine_mode(cycle_mode: str, cycle_object: object):
    """
    Sort through based on mode
    and process conditionals if
    active and .history.json item
    does not exist.
    """

    cycle_active = cycle_object["active"]

    if cycle_active:
        if not history.item_exists(cycle_mode, cycle_object):
            process_mode(
                cycle_mode,
                cycle_object
            )

def process_items():
    """
    Iterate over cycles.json and
    process down and up cycle jobs.
    """

    datafile.create_json(constants.CYCLES_PATH)
    datafile.create_json(constants.HISTORY_PATH)

    for cycle_object in datafile.read_json(constants.CYCLES_PATH):
        determine_mode(
            "down",
            cycle_object
        )

        determine_mode(
            "up",
            cycle_object
        )
