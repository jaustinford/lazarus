"""
Manage schedule-type jobs objects and
increment according to time operators.
"""

from datetime import datetime, timedelta

import constants
import logs
import datafile

LOGGER = logs.logging.getLogger(__name__)

def increment_days(trigger_date: str, schedule_type: str):
    """
    Return date string adding the
    current time with the delta from
    'trigger_date', in days.
    """

    job_mode_dt = datetime.strptime(trigger_date, constants.DATE_FORMAT)

    if schedule_type == "daily":
        delta_date_dt = job_mode_dt + timedelta(days=1)

    elif schedule_type == "weekly":
        delta_date_dt = job_mode_dt + timedelta(days=7)

    elif schedule_type.startswith("customdays"):
        delta_date_days = int(schedule_type.split(":")[1])
        delta_date_dt   = job_mode_dt + timedelta(days=delta_date_days)

    delta_date_string = delta_date_dt.strftime(constants.DATE_FORMAT)
    job_delta_string  = schedule_type + " - " + delta_date_string

    LOGGER.info("Incrementing scheduled job by days : %s", job_delta_string)

    return delta_date_string

def increment_hours(trigger_time: str, schedule_type: str):
    """
    Return time string adding the
    current time with the delta from
    'trigger_time', in hours.
    """

    job_mode_dt = datetime.strptime(trigger_time, constants.TIME_FORMAT)

    if schedule_type == "hourly":
        delta_time_dt = job_mode_dt + timedelta(hours=1)

    elif schedule_type.startswith("customhours"):
        delta_time_hours = int(schedule_type.split(":")[1])
        delta_time_dt    = job_mode_dt + timedelta(hours=delta_time_hours)

    delta_time_string = delta_time_dt.strftime(constants.TIME_FORMAT)
    job_time_string   = schedule_type + " - " + delta_time_string

    LOGGER.info("Incrementing scheduled job by hours : %s", job_time_string)

    return delta_time_string

def create_object(job_object: object):
    """
    Direct incrementation of datetime
    fields based on 'job_type' values.
    """

    job_id           = datafile.generate_id()
    job_type         = job_object["type"]
    job_mode         = job_object["mode"]
    job_trigger_date = job_object["trigger"]["date"]
    job_trigger_time = job_object["trigger"]["time"]

    schedule_type      = job_type.split(":")[1:]
    schedule_type_join = ":".join(schedule_type)

    if schedule_type_join.startswith(("daily", "weekly", "customdays")):
        incremented_days  = increment_days(job_trigger_date, schedule_type_join)
        incremented_hours = job_trigger_time

    elif schedule_type_join.startswith(("hourly", "customhours")):
        incremented_days  = job_trigger_date
        incremented_hours = increment_hours(job_trigger_time, schedule_type_join)

    LOGGER.info("Creating schedule job : %s", job_id)

    return {
        "id": job_id,
        "type": job_type,
        "mode": job_mode,
        "trigger": {
            "date": incremented_days,
            "time": incremented_hours
        }
    }
