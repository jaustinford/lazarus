"""
Monitor UPS metric data to determine
when to execute power cycle jobs as
well as ingest UPS metric data to
Elasticsearch.
"""

import os
import time

import constants
import cycles
import apc

def main():
    """
    Main loop execution.
    """

    increment_counter = 0

    apc.service_init()

    while True:
        if increment_counter == 20:
            if not os.path.isfile(constants.CYCLES_LOCK_PATH):
                apc.process_elastic()

            increment_counter = 0

        increment_counter += 1

        cycles.process_items()
        time.sleep(1)

if __name__ == "__main__":
    main()
