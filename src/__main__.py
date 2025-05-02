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

    for conf_file in apc.find_conf_files(constants.CONF_DIR):
        logs.GENERAL_LOGGER.info("Starting APC daemon against conf file : %s", conf_file)
        apc.start_daemon(conf_file)

    increment_counter = 0

    while True:
        if not os.path.isfile(constants.CYCLES_LOCK_PATH) and \
           increment_counter == 30:
            logs.GENERAL_LOGGER.info("test")
            es_client = elastic.connect_elasticsearch()
            logs.GENERAL_LOGGER.info(es_client.info(filter_path="cluster_name"))

            if not es_client.indices.exists(index="apcups"):
                elastic.create_index(es_client, "apcups")

            for combined_metric in apc.combine_metrics(constants.CONF_DIR):
                logs.GENERAL_LOGGER.info("combined test : %s", str(combined_metric))
                es_client.index(
                    index="apcups",
                    document=combined_metric
                )

            increment_counter = 0

            es_client.close()

        increment_counter += 1

        cycles.process_items()
        time.sleep(1)

if __name__ == "__main__":
    main()
