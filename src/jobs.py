"""
Manage a persisted JSON data file
for tracking the various job
operations.
"""

import os
from datetime import datetime, timedelta

import constants
import logs
import datafile

def manage_lock(lock_mode: str, job_object: object):
    """
    Use a lock file to skip certain
    operations until lock file is
    removed.
    """

    if lock_mode == "add":
        if not os.path.isfile(constants.DOWN_LOCK_PATH):
            logs.GENERAL_LOGGER.info("Creating down lock file : %s", constants.DOWN_LOCK_PATH)
            with open(constants.DOWN_LOCK_PATH, "w", encoding="utf-8") as down_lock_opened:
                down_lock_opened.write(job_object["id"])

    elif lock_mode == "remove":
        if os.path.isfile(constants.DOWN_LOCK_PATH):
            logs.GENERAL_LOGGER.info("Removing down lock file : %s", constants.DOWN_LOCK_PATH)
            os.remove(constants.DOWN_LOCK_PATH)

def add_object(job_object: object):
    """
    Return a list of all jobs objects, plus
    the one provided in 'job_object'.
    """

    added_list = []

    for file_object in datafile.read_json(constants.JOBS_PATH):
        added_list.append(file_object)

    added_list.append(job_object)

    return added_list

def remove_object(job_object: object):
    """
    Return a list of all jobs objects, less
    the one provided in 'job_object'.
    """

    removed_list = []

    job_id = job_object["id"]

    for file_object in datafile.read_json(constants.JOBS_PATH):
        if file_object["id"] != job_id:
            removed_list.append(file_object)

    return removed_list

def trigger_object(trigger_date: str, trigger_time: str):
    """
    Decide whether a job is
    conditional to run, based
    on datetime in 'trigger_date'.
    """

    should_run = False

    trigger_datetime = trigger_date + "T" + trigger_time + "Z"

    real_time_dt   = datetime.now().replace(microsecond=0)
    target_time_dt = datetime.strptime(trigger_datetime, constants.DATETIME_FORMAT)
    delta_time_dt  = target_time_dt + timedelta(seconds=5)

    if real_time_dt >= target_time_dt:
        if real_time_dt < delta_time_dt:
            should_run = True

    return should_run
