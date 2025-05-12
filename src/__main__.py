"""
Execute IAC-Configure down or up
cycles given different kinds of
events.
"""

import os
import time

import constants
import execute
import apc

def main():
    """
    Grab metric data and upload to Elasticsearch
    every 'constants.ELASTIC_INGEST_INTERVAL'
    number of seconds, then process jobs.json
    items.
    """

    elastic_counter = 0

    apc.service_init()

    while True:
        combined_metrics = apc.combine_metrics(constants.CONF_DIR)

        if elastic_counter == constants.ELASTIC_INGEST_INTERVAL:
            if not os.path.isfile(constants.DOWN_LOCK_PATH):
                apc.process_elastic(combined_metrics)

            elastic_counter = 0

        elastic_counter += 1

        execute.process_ingest()
        execute.process_jobs(combined_metrics)
        time.sleep(1)

if __name__ == "__main__":
    main()
