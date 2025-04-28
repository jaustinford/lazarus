"""
Manage a persisted file for tracking
the various cycle operations.
"""

import os
import json
import datetime
import logs
import history

logger = logs.logging.getLogger(__name__)

def create_json(cycles_file: str):
    """
    Create the cycles.json file
    if missing.
    """

    if not os.path.isfile(cycles_file):
        logger.info("Creating cycles file : %s", cycles_file)
        with open(cycles_file, "w", encoding="utf-8") as history_opened:
            history_opened.write(
                json.dumps(
                    {
                        "cycles": []
                    },
                    indent=2
                )
            )

def read_json(cycles_file: str):
    """
    Open cycles.json file and assign as
    a JSON object.
    """

    with open(cycles_file, "r", encoding="utf-8") as cycles_opened:
        cycles_read = cycles_opened.read()
        cycles_json = json.loads(cycles_read)["cycles"]

    return cycles_json

def process_mode(history_file: str, cycle_mode: str, cycle_object: object):
    """
    Conditionally execute targetted
    mode and evaluate the real_time
    timestamp.
    """

    cycle_id   = cycle_object["id"]
    cycle_down = cycle_object["down"]
    cycle_up   = cycle_object["up"]

    if cycle_mode == "down":
        mode_time = cycle_down

    elif cycle_mode == "up":
        mode_time = cycle_up

    should_run = False

    real_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    if mode_time == "now":
        should_run = True

        logger.info(
            "Executing non-scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    elif mode_time == real_time:
        should_run = True

        logger.info(
            "Executing scheduled cycle %s", cycle_mode + " job : " + cycle_id
        )

    if should_run:
        history.update_json(
            history_file,
            cycle_mode,
            cycle_object
        )

        os.environ["CYCLE_MODE"] = cycle_mode
        os.system("python /iac-configure/triggers/profile.py > /dev/null")

def determine_mode(history_file: str, cycle_mode: str, cycle_object: object):
    """
    Sort through based on mode
    and process conditionals if
    active and .history.json item
    does not exist.
    """

    cycle_active = cycle_object["active"]

    if cycle_active:
        if not history.item_exists(history_file, cycle_mode, cycle_object):
            process_mode(
                history_file,
                cycle_mode,
                cycle_object
            )

def process_items(cycles_file: str, history_file: str):
    """
    Iterate over cycles.json and
    process down and up cycle jobs.
    """

    create_json(cycles_file)
    history.create_json(history_file)

    for cycle_object in read_json(cycles_file):
        determine_mode(
            history_file,
            "down",
            cycle_object
        )

        determine_mode(
            history_file,
            "up",
            cycle_object
        )
