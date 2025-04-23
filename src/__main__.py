"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time
import apc

FILE_PATH   = os.path.abspath(__file__)
SRC_DIR     = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(SRC_DIR)
CONF_DIR    = os.path.join(PROJECT_DIR, "conf")

def find_conf_files():
    """
    Return a list of the conf files
    presented in /lazarus/conf.
    """

    conf_files = []

    for conf_file in os.listdir(CONF_DIR):
        conf_files.append(
            os.path.join(CONF_DIR, conf_file)
        )

    return conf_files

def find_ups_nisport(conf_file: str):
    """
    Read the conf file for a given UPS
    and return the configured NISPORT.
    """

    with open(conf_file, "r", encoding="utf-8") as conf_opened:
        conf_lines = conf_opened.readlines()

    for conf_line in conf_lines:
        if conf_line.startswith("NISPORT"):
            port_value = conf_line.split(" ")[1]
            break

    if not port_value:
        port_value = None

    return int(port_value)

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    for conf_file in find_conf_files():
        apc.start_daemon(conf_file)

    while True:
        combined_metrics = []

        for conf_file in find_conf_files():
            ups_metrics = apc.get_metrics(
                find_ups_nisport(conf_file)
            )

            combined_metrics.append(
                {
                    ups_metrics["UPSNAME"]: {
                        "status": ups_metrics["STATUS"],
                        "timeleft": ups_metrics["TIMELEFT"].split(" ")[0],
                        "bcharge": ups_metrics["BCHARGE"].split(" ")[0],
                        "loadpct": ups_metrics["LOADPCT"].split(" ")[0]
                    }
                }
            )

        print("test - " + combined_metrics)

        time.sleep(10)

if __name__ == "__main__":
    main()
