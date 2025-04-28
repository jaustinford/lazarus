"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time
import logs
# import apc
import cycles

logger = logs.logging.getLogger(__name__)

FILE_PATH    = os.path.abspath(__file__)
SRC_DIR      = os.path.dirname(FILE_PATH)
PROJECT_DIR  = os.path.dirname(SRC_DIR)

CONF_DIR     = os.path.join(PROJECT_DIR, "conf")
CYCLES_FILE  = os.path.join(PROJECT_DIR, "cycles.json")
HISTORY_FILE = os.path.join(PROJECT_DIR, ".history.json")

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    # for conf_file in find_conf_files(CONF_DIR):
    #     logger.info("Starting APC daemon against conf file : %s", conf_file)
    #     apc.start_daemon(conf_file)

    while True:
        # combined_metrics = apc.combine_metrics()

        cycles.process_items(CYCLES_FILE, HISTORY_FILE)

        time.sleep(1)

if __name__ == "__main__":
    main()
