"""
Manage power event objects and
increment using UPS metric data.
"""

from datetime import datetime, timedelta

import constants
import logs
import datafile
import apc

def increment_minutes(job_mode: str, combined_metrics: list):
    """
    Return datetime for power 'down'
    and 'up' events adjusting timedelta
    against UPS 'timeleft' metrics.
    """

    real_time_dt = datetime.now().replace(microsecond=0)

    if job_mode == "down":
        battery_remain = \
            apc.retrieve_min("timeleft", combined_metrics) - constants.POWER_MIN_BATTERY_DOWN

        delta_time_dt  = real_time_dt + timedelta(minutes=battery_remain)

    elif job_mode == "up":
        delta_time_dt = real_time_dt

    delta_time_string = datetime.strftime(delta_time_dt, constants.DATETIME_FORMAT)
    job_delta_string  = job_mode + ":" + delta_time_string

    logs.GENERAL_LOGGER.info("Incrementing power job by minutes : %s", job_delta_string)

    return delta_time_dt

def create_object(job_mode: str, combined_metrics: list):
    """
    Generate a power object against
    recently polled UPS metric data.
    """

    job_id = datafile.generate_id()

    logs.GENERAL_LOGGER.info("Creating power job : %s", job_id)

    return {
        "id": datafile.generate_id(),
        "type": "power",
        "mode": job_mode,
        "trigger": {
            "date": str(increment_minutes(job_mode, combined_metrics).date()),
            "time": str(increment_minutes(job_mode, combined_metrics).time())
        }
    }
