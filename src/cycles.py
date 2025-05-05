"""
Manage a persisted JSON data file
for tracking the various cycle
operations.
"""

import os
import re
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

def increment_date(cycle_type: str, cycle_job: str):
    """
    Generate future dates for down and up
    job cycles respective of the month.
    """

    cycle_job_month = cycle_job.split(" ")[0].split("-")[1]
    cycle_job_day   = cycle_job.split(" ")[0].split("-")[2]

    if cycle_type == "daily":
        day_increment = 1

    elif cycle_type == "weekly":
        day_increment = 7

    new_cycle_down_day = int(cycle_job_day) + day_increment

    if new_cycle_down_day > constants.MONTHS[cycle_job_day]:
        new_cycle_down_day   = new_cycle_down_day - constants.MONTHS[cycle_job_day]
        new_cycle_down_month = int(cycle_job_month) + 1

        if new_cycle_down_month > 12:
            new_cycle_down_month == 1

    else:
        new_cycle_down_month = cycle_job_month

    if new_cycle_down_day < 10:
        new_cycle_down_day = "0" + str(new_cycle_down_day)

    substituted_month = re.sub(
        "-" + cycle_job_month + "-",
        "-" + str(new_cycle_down_month) + "-",
        cycle_job
    )

    substituted_day = re.sub(
        "-" + cycle_job_day + " ",
        "-" + str(new_cycle_down_day) + " ",
        substituted_month
    )

    return substituted_day

def scheduled_job(cycle_object: object):
    """
    Create scheduled job object with generated
    timestamps reflecting incremented times.
    """

    cycle_type = cycle_object["type"]
    cycle_down = cycle_object["down"]
    cycle_up   = cycle_object["up"]

    new_scheduled_obect = {
        "id": "generate_random_id()",
        "type": cycle_type,
        "down": increment_date(cycle_type, cycle_down),
        "up": increment_date(cycle_type, cycle_up)
    }

    return new_scheduled_obect

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

    if cycle_type == "daily" or \
       cycle_type == "weekly":
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

    real_time = datetime.datetime.now().strftime(constants.TIME_FORMAT_CYCLE)

    if cycle_mode == "down":
        mode_time = cycle_down

    elif cycle_mode == "up":
        mode_time = cycle_up

    if mode_time == "now":
        should_run = True

    elif mode_time == real_time:
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
