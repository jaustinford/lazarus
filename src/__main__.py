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

    elastic_counter = 0
    power_counter   = (0, 0, 0, 0)

    apc.service_init()

    while True:
        combined_metrics = apc.combine_metrics(constants.CONF_DIR)
        elastic_counter  = execute.process_elastic(combined_metrics, elastic_counter)
        power_counter    = execute.process_power(combined_metrics, power_counter)

        execute.process_ingest()
        execute.process_jobs()

        time.sleep(1)

if __name__ == "__main__":
    main()
