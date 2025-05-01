"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time
import logs
import cycles
import apc
import elastic

LOGGER = logs.logging.getLogger(__name__)

FILE_PATH   = os.path.abspath(__file__)
SRC_DIR     = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(SRC_DIR)

CONF_DIR     = os.path.join(PROJECT_DIR, "conf")
DATA_DIR     = os.path.join(PROJECT_DIR, "data")
CYCLES_PATH  = os.path.join(PROJECT_DIR, DATA_DIR, "cycles.json")
HISTORY_PATH = os.path.join(PROJECT_DIR, DATA_DIR, ".history.json")

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    es_client = elastic.connect_elasticsearch()

    increment_counter = 0

    if es_client.ping():
        if not es_client.indices.exists(index="apcups"):
            elastic.create_index(es_client, "apcups")

    for conf_file in apc.find_conf_files(CONF_DIR):
        LOGGER.info("Starting APC daemon against conf file : %s", conf_file)
        apc.start_daemon(conf_file)

    while True:
        increment_counter += 1

        if es_client.ping() and increment_counter == 30:
            for combined_metric in apc.combine_metrics(CONF_DIR):
                es_client.index(
                    index="apcups",
                    document=combined_metric
                )

            increment_counter = 0

        cycles.process_items(
            CYCLES_PATH,
            HISTORY_PATH
        )

        time.sleep(1)

if __name__ == "__main__":
    main()
