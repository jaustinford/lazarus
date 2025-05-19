"""
Execute IAC-Configure down or up
cycles given different kinds of
events.
"""

import time

import constants
import execute
import apc

def main():
    """
    Run project process functions over
    iterated while loop.
    """

    apc.service_init()

    elastic_counter = 0

    while True:
        combined_metrics = apc.combine_metrics(constants.CONF_DIR)

        execute.process_ingest()

        elastic_counter = execute.process_elastic(combined_metrics, elastic_counter)

        execute.process_power(combined_metrics)
        execute.process_jobs()

        time.sleep(1)

if __name__ == "__main__":
    main()
