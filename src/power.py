"""
Manage power event objects and
increment using UPS metric data.
"""

import os
from datetime import datetime

import constants
import logs
import datafile
import apc
import jobs

def clear_event():
    """
    Run tasks to clear power event.
    """

    power_lock = os.path.join(constants.DATA_DIR, "power.lock")

    if jobs.find_object("power", "down"):
        retrieved_object = jobs.retrieve_object("power", "down")
        removed_list     = jobs.remove_object(retrieved_object)

        datafile.write_json(constants.JOBS_PATH, removed_list)

        logs.GENERAL_LOGGER.info("UPS power event has cleared.")

    if not jobs.find_object("power", "up"):
        if os.path.isfile(power_lock):
            power_object = create_object("up")
            added_list   = jobs.add_object(power_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

def trigger_event():
    """
    Run tasks to trigger power event.
    """

    power_lock = os.path.join(constants.DATA_DIR, "power.lock")

    if not os.path.isfile(power_lock):
        if not jobs.find_object("power", "down"):
            logs.GENERAL_LOGGER.info("UPS power event has occurred.")

            power_object = create_object("down")
            added_list   = jobs.add_object(power_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

        else:
            retrieved_object = jobs.retrieve_object("power", "down")
            removed_list     = jobs.remove_object(retrieved_object)

            datafile.write_json(constants.JOBS_PATH, removed_list)

            power_object = create_object("down")
            added_list   = jobs.add_object(power_object)

            datafile.write_json(constants.JOBS_PATH, added_list)

def determine_event(status_value: str, combined_metrics: list, mode_counter: tuple):
    """
    Increment counters to determine that
    'status_value' has maintained
    cumulatively over 'constants.POWER_STATUS_INTERVAL'
    seconds against a period of
    'constants.POWER_EVENT_INTERVAL' seconds.
    """

    should_trigger = False

    status_counter = mode_counter[0]
    event_counter  = mode_counter[1]

    power_lock = os.path.join(constants.DATA_DIR, "power.lock")

    if status_value == "ONBATT":
        event_interval  = constants.POWER_TRIGGER_EVENT_INTERVAL
        status_interval = constants.POWER_TRIGGER_STATUS_INTERVAL

        if apc.ensure_status_any("ONBATT", combined_metrics):
            status_counter += 1
            event_counter  += 1

        else:
            if event_counter >= 1:
                event_counter += 1

    elif status_value == "ONLINE":
        if os.path.isfile(power_lock):
            event_interval  = constants.POWER_CLEAR_EVENT_INTERVAL
            status_interval = constants.POWER_CLEAR_STATUS_INTERVAL

            if apc.ensure_status_all("ONLINE", combined_metrics):
                status_counter += 1
                event_counter  += 1

            else:
                if event_counter >= 1:
                    event_counter += 1

    if event_counter == event_interval:
        if status_counter >= status_interval:
            should_trigger = True
            status_counter = 0

        event_counter = 0

    return (should_trigger, status_counter, event_counter)

def create_object(job_mode: str):
    """
    Generate a power object against
    recently polled UPS metric data.
    """

    job_id      = datafile.generate_id()
    job_trigger = datetime.now().replace(microsecond=0)

    logs.GENERAL_LOGGER.info("Creating power job : %s", job_id)

    return {
        "id": job_id,
        "type": "power",
        "mode": job_mode,
        "trigger": {
            "date": str(job_trigger.date()),
            "time": str(job_trigger.time())
        }
    }
