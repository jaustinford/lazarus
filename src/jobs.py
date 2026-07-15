"""
Manage a persisted JSON data file
for tracking the various job
operations.
"""

import os
import re
from datetime import datetime, timedelta

import constants
import datafile

MAIN_LOG = constants.logging.getLogger(__name__)

def find_locks():
    """
    Return true if any of the
    lock files exist in 'DATA_DIR'.
    """

    locks_found = False

    for file_name in os.listdir(constants.DATA_DIR):
        if file_name.endswith(".lock"):
            locks_found = True
            break

    return locks_found

def manage_lock(lock_mode: str, job_object: object):
    """
    Use a lock file to skip certain
    operations until lock file is
    removed.
    """

    job_type       = job_object["type"]
    job_type_title = re.sub(":", "-", job_type)

    job_lock = os.path.join(
        constants.DATA_DIR,
        job_type_title + ".lock"
    )

    if lock_mode == "add":
        if not os.path.isfile(job_lock):
            MAIN_LOG.info("Creating lock file : %s", job_lock)

            with open(job_lock, "w", encoding="utf-8") as down_lock_opened:
                down_lock_opened.write(job_object["id"])

    elif lock_mode == "remove":
        if os.path.isfile(job_lock):
            MAIN_LOG.info("Removing lock file : %s", job_lock)

            os.remove(job_lock)

def add_object(job_object: object):
    """
    Return a list of all jobs objects, plus
    the one provided in 'job_object'.
    """

    added_list = []

    job_id = job_object["id"]

    for file_object in datafile.read_json(constants.JOBS_FILE):
        added_list.append(file_object)

    MAIN_LOG.info("Adding object to jobs.json : %s", job_id)
    added_list.append(job_object)

    return added_list

def remove_object(job_object: object):
    """
    Return a list of all jobs objects, less
    the one provided in 'job_object'.
    """

    removed_list = []

    job_id = job_object["id"]

    for file_object in datafile.read_json(constants.JOBS_FILE):
        if file_object["id"] != job_id:
            removed_list.append(file_object)

    MAIN_LOG.info("Removing object from jobs.json : %s", job_id)

    return removed_list

def trigger_object(trigger_date: str, trigger_time: str):
    """
    Decide whether a job is
    conditional to run, based
    on datetime in 'trigger_date'.
    """

    should_run = False

    trigger_datetime_string = trigger_date + "T" + trigger_time + "Z"

    real_time_dt   = datetime.now().replace(microsecond=0)
    target_time_dt = datetime.strptime(trigger_datetime_string, constants.DATETIME_FORMAT)
    delta_time_dt  = target_time_dt + timedelta(seconds=constants.JOB_EXECUTE_DELTA)

    if real_time_dt >= target_time_dt:
        if real_time_dt < delta_time_dt:
            MAIN_LOG.info("Trigger event has occured")
            should_run = True

    return should_run

def find_object(job_type: str, job_mode: str):
    """
    Return true if object exists
    in jobs.json.
    """

    power_found = False

    for file_object in datafile.read_json(constants.JOBS_FILE):
        object_type = file_object["type"]
        object_mode = file_object["mode"]

        if object_type == job_type:
            if object_mode == job_mode:
                power_found = True
                break

    return power_found

def retrieve_object(job_type: str, job_mode: str):
    """
    Return an existing object from
    jobs.json based on 'object_type'
    and 'object_mode'.
    """

    found_object = {}

    for file_object in datafile.read_json(constants.JOBS_FILE):
        object_type = file_object["type"]
        object_mode = file_object["mode"]

        if object_type == job_type:
            if object_mode == job_mode:
                found_object = file_object
                break

    return found_object
