"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time

import constants
import logs
import cycles
import apc
import elastic

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    increment_counter = 0

    for conf_file in apc.find_conf_files(constants.CONF_DIR):
        logs.GENERAL_LOGGER.info("Starting APC daemon against conf file : %s", conf_file)
        apc.start_daemon(conf_file)

    while True:
        increment_counter += 1

        if not os.path.isfile(constants.CYCLES_LOCK_PATH):
            es_client = elastic.connect_elasticsearch()

            if not es_client.indices.exists(index="apcups"):
                elastic.create_index(es_client, "apcups")

            if increment_counter == 30:
                for combined_metric in apc.combine_metrics(constants.CONF_DIR):
                    es_client.index(
                        index="apcups",
                        document=combined_metric
                    )

                increment_counter = 0

        cycles.process_items(
            constants.CYCLES_LOCK_PATH,
            constants.CYCLES_PATH,
            constants.HISTORY_PATH
        )

        time.sleep(1)

if __name__ == "__main__":
    main()
