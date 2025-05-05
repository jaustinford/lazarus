"""
Manage a persisted JSON data file
for tracking the various cycle
operations.
"""

import os
import random
import string
from datetime import datetime, timedelta

import constants
import logs
import datafile
import apc
import history

def generate_random_id(string_length: int=20):
    """
    Create a random string given
    string_length.
    """

    random_string = ""

    for _ in range(string_length):
        random_string += random.choice(
            string.ascii_lowercase + string.ascii_uppercase
        )

    return random_string

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

def increment_date(cycle_type: str, cycle_job: str):
    """
    Generate future dates for down and up
    job cycles using timedelta.
    """

    cycle_job_dt = datetime.strptime(cycle_job, constants.TIME_FORMAT)

    if cycle_type == "daily":
        delta_time_dt = cycle_job_dt + timedelta(days=1)

    elif cycle_type == "weekly":
        delta_time_dt = cycle_job_dt + timedelta(days=7)

    elif cycle_type.startswith("custom"):
        delta_time_days = int(cycle_type.split(":")[1])
        delta_time_dt   = cycle_job_dt + timedelta(days=delta_time_days)

    delta_time_string = delta_time_dt.strftime(constants.TIME_FORMAT)

    return delta_time_string

def scheduled_job(cycle_object: object):
    """
    Create scheduled job object with generated
    timestamps reflecting incremented times.
    """

    cycle_type = cycle_object["type"]
    cycle_down = cycle_object["down"]
    cycle_up   = cycle_object["up"]

    new_scheduled_obect = {
        "id": generate_random_id(),
        "type": cycle_type,
        "down": increment_date(cycle_type, cycle_down),
        "up": increment_date(cycle_type, cycle_up)
    }

    return new_scheduled_obect

def add_object(cycle_object: object):
    """
    Return a list of all cycles object, plus
    the one provided in cycle_object.
    """

    added_list = []

    for file_object in datafile.read_json(constants.CYCLES_PATH):
        added_list.append(file_object)

    added_list.append(cycle_object)

    return added_list

def remove_object(cycle_object: object):
    """
    Return a list of all cycles object, less
    the one provided in cycle_object.
    """

    removed_list = []

    cycle_id   = cycle_object["id"]
    cycle_type = cycle_object["type"]

    for file_object in datafile.read_json(constants.CYCLES_PATH):
        if file_object["id"] != cycle_id:
            removed_list.append(file_object)

    if cycle_type in "daily" "weekly":
        removed_list.append(
            scheduled_job(cycle_object)
        )

    elif cycle_type.startswith("custom"):
        removed_list.append(
            scheduled_job(cycle_object)
        )

    return removed_list

def evaluate_object(cycle_mode: str, cycle_object: object):
    """
    Decide whether a cycle is
    conditional to run.
    """

    cycle_id   = cycle_object["id"]
    cycle_type = cycle_object["type"]
    cycle_down = cycle_object["down"]
    cycle_up   = cycle_object["up"]

    should_run = False

    if cycle_mode == "down":
        mode_time = cycle_down

    elif cycle_mode == "up":
        mode_time = cycle_up

    real_time_dt   = datetime.now().replace(microsecond=0)
    target_time_dt = datetime.strptime(mode_time, constants.TIME_FORMAT)
    delta_time_dt  = target_time_dt + timedelta(seconds=5)

    if real_time_dt >= target_time_dt:
        if real_time_dt < delta_time_dt:
            should_run = True

    if should_run:
        logs.GENERAL_LOGGER.info(
            "Selecting %s", cycle_type + " type " + cycle_mode + " job : " + cycle_id
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

        logs.GENERAL_LOGGER.info("Executing IAC-Configure in %s", cycle_mode + " mode...")
        os.environ["CYCLE_MODE"] = cycle_mode
        os.system("python /iac-configure/triggers/profile.py > /dev/null 2>&1")

        if cycle_mode == "up":
            datafile.write_json(
                constants.CYCLES_PATH,
                remove_object(cycle_object)
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

    if not history.item_exists(cycle_mode, cycle_object):
        process_mode(
            cycle_mode,
            cycle_object
        )

def process_items(combined_metrics: list):
    """
    Iterate over cycles.json and
    process down and up cycle jobs.
    """

    datafile.create_json(constants.CYCLES_PATH)
    datafile.create_json(constants.HISTORY_PATH)

    if apc.determine_power_event(combined_metrics):
        logs.GENERAL_LOGGER.info("Power event has occurred.")

    for cycle_object in datafile.read_json(constants.CYCLES_PATH):
        determine_mode(
            "down",
            cycle_object
        )

        determine_mode(
            "up",
            cycle_object
        )
