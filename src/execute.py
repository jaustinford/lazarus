"""
Organizing workflow for managing
objects within jobs.json.
"""

import os

import constants
import logs
import datafile
import ingest
import apc
import jobs
import schedule
import power

def run_cycle(job_mode: str):
    """
    Run the IAC-Configure playbook given
    CYCLE_MODE as either 'up' or 'down'.
    """

    logs.GENERAL_LOGGER.info("Executing IAC-Configure in %s", job_mode + " mode...")
    os.environ["CYCLE_MODE"] = job_mode
    # os.system("python /iac-configure/triggers/profile.py > /dev/null 2>&1")
    logs.GENERAL_LOGGER.info("Completed IAC-Configure in %s", job_mode + " mode...")

def process_schedule(job_object: object):
    """
    Direct objects of type 'schedule:' and
    follow along to increment respective datetime
    fields.
    """

    job_type = job_object["type"]

    if job_type.startswith("schedule"):
        schedule_object = schedule.create_object(job_object)

        added_list = jobs.add_object(schedule_object)
        datafile.write_json(constants.JOBS_PATH, added_list)

def process_power(combined_metrics: list):
    """
    Conditionalize the creation of power
    event objects in jobs.json.
    """

    if not apc.ensure_status("ONLINE", combined_metrics):
        if not jobs.find_object("power", "down"):
            logs.GENERAL_LOGGER.info("UPS power event has occurred.")

            power_object = power.create_object("down", combined_metrics)
            added_list   = jobs.add_object(power_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

        else:
            retrieved_object = jobs.retrieve_object("power", "down")
            removed_list     = jobs.remove_object(retrieved_object)

            datafile.write_json(constants.JOBS_PATH, removed_list)

            power_object = power.create_object("down", combined_metrics)
            added_list   = jobs.add_object(power_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

    else:
        if jobs.find_object("power", "down"):
            retrieved_object = jobs.retrieve_object("power", "down")
            removed_list     = jobs.remove_object(retrieved_object)

            datafile.write_json(constants.JOBS_PATH, removed_list)

        if not jobs.find_object("power", "up"):
            if apc.retrieve_min("timeleft", combined_metrics) >= constants.POWER_MIN_BATTERY_TOTAL:
                power_lock = os.path.join(constants.DATA_DIR, "power.lock")

                if os.path.isfile(power_lock):
                    power_object = power.create_object("up", combined_metrics)
                    added_list   = jobs.add_object(power_object)

                    datafile.write_json(constants.JOBS_PATH, added_list)

def process_mode(job_object: object):
    """
    Determine if timedate for object has
    been met, then manage lock and jobs.json
    files.
    """

    job_mode         = job_object["mode"]
    job_type         = job_object["type"]
    job_trigger_date = job_object["trigger"]["date"]
    job_trigger_time = job_object["trigger"]["time"]

    if jobs.trigger_object(job_trigger_date, job_trigger_time):
        removed_list = jobs.remove_object(job_object)

        if job_mode == "down":
            jobs.manage_lock("add", job_object)
            datafile.write_json(constants.JOBS_PATH, removed_list)

            if job_type.startswith("schedule"):
                process_schedule(job_object)

        run_cycle(job_mode)

        if job_mode == "up":
            jobs.manage_lock("remove", job_object)
            datafile.write_json(constants.JOBS_PATH, removed_list)

            if job_type.startswith("schedule"):
                process_schedule(job_object)

def process_ingest():
    """
    Read ingest.csv and generate jobs.json
    objects for each line.
    """

    ingest.create_file(constants.INGEST_PATH)

    ingest_readlines = ingest.read_file(constants.INGEST_PATH)

    if ingest_readlines:
        ingest_list = ingest.create_jobs(ingest_readlines)

        for ingest_object in ingest_list:
            added_list = jobs.add_object(ingest_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

        ingest.clear_file(constants.INGEST_PATH)

def process_jobs():
    """
    Iterate over jobs.json and
    process each item.
    """

    datafile.create_json(constants.JOBS_PATH)

    for job_object in datafile.read_json(constants.JOBS_PATH):
        process_mode(job_object)
