"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time
from apcaccess import status

FILE_PATH   = os.path.abspath(__file__)
DIR_FILE    = os.path.dirname(FILE_PATH)
DIR_PROJECT = os.path.dirname(DIR_FILE)
CONF_DIR    = os.path.join(DIR_PROJECT, "conf")

def start_acpupsd(ups_name: str):
    """
    Start apcupsd daemon and bind a
    localhost TCP port.
    """

    os.system(
        "/sbin/apcupsd \
            -f /etc/apcupsd/" + ups_name + ".conf"
    )

def apc_get_metrics(daemon_port: int):
    """
    Poll the UPS for the latest metrics,
    given the port of the daemon.
    """

    ups_metrics = status.parse(
        status.get(port=daemon_port)
    )

    return ups_metrics

def find_ups_nisport(ups_name: str):
    """
    Read the conf file for a given UPS
    and return the configured NISPORT.
    """

    conf_file = os.path.join(CONF_DIR, ups_name + ".conf")

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

    start_acpupsd("ups-0")
    start_acpupsd("ups-1")

    while True:
        ups0_metrics = apc_get_metrics(
            find_ups_nisport("ups-0")
        )

        ups1_metrics = apc_get_metrics(
            find_ups_nisport("ups-1")
        )

        print(ups0_metrics)
        print(" ")
        print(ups1_metrics)

        time.sleep(10)

if __name__ == "__main__":
    main()
