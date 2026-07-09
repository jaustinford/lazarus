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

LOGGER = logs.logging.getLogger(__name__)

def add_event(event_type: str, event_mode: str):
    """
    Run tasks to create power event which
    can be one of two 'event_type's :
    'trigger' or 'clear'.
    """

    LOGGER.info("Power event has been confirmed : %s", event_type)

    power_object = create_object(event_mode)
    added_list   = jobs.add_object(power_object)

    datafile.write_json(constants.JOBS_FILE, added_list)

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
        status_interval = constants.POWER_TRIGGER_STATUS_INTERVAL
        event_interval  = constants.POWER_TRIGGER_EVENT_INTERVAL

        if apc.ensure_status_any("ONBATT", combined_metrics):
            status_counter += 1
            event_counter  += 1

        else:
            if event_counter >= 1:
                event_counter += 1

        if apc.ensure_status_any("ONBATT", combined_metrics):
            LOGGER.info(
                "Qualifying power trigger event : %s",
                "status ( " + str(status_counter) + " ) | " + \
                "event ( " + str(event_counter) + " )"
            )

    elif status_value == "ONLINE":
        status_interval = constants.POWER_CLEAR_STATUS_INTERVAL
        event_interval  = constants.POWER_CLEAR_EVENT_INTERVAL

        if os.path.isfile(power_lock):
            if apc.ensure_status_all("ONLINE", combined_metrics):
                status_counter += 1
                event_counter  += 1

            else:
                if event_counter >= 1:
                    event_counter += 1

            if apc.ensure_status_all("ONLINE", combined_metrics):
                LOGGER.info(
                    "Qualifying power clear event : %s",
                    "status ( " + str(status_counter) + " ) | " + \
                    "event ( " + str(event_counter) + " )"
                )

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

    LOGGER.info("Creating power job : %s", job_id)

    return {
        "id": job_id,
        "type": "power",
        "mode": job_mode,
        "trigger": {
            "date": str(job_trigger.date()),
            "time": str(job_trigger.time())
        }
    }
