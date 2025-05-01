"""
Parse results from the apcaccess
library and manage daemon.
"""

import os
import time
import datetime
from apcaccess import status

def start_daemon(conf_file: str):
    """
    Start apcupsd daemon and bind a
    localhost TCP port.
    """

    os.system(
        "/sbin/apcupsd \
            -f " + conf_file
    )

    time.sleep(10)

def get_metrics(daemon_port: int):
    """
    Poll the UPS for the latest metrics,
    given the port of the daemon.
    """

    ups_metrics = status.parse(
        status.get(
            host="localhost",
            port=daemon_port
        )
    )

    return ups_metrics

def find_conf_files(conf_dir: str):
    """
    Return a list of the conf files
    presented in /lazarus/conf.
    """

    conf_files = []

    for conf_file in os.listdir(conf_dir):
        conf_files.append(
            os.path.join(conf_dir, conf_file)
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

def combine_metrics(conf_dir: str):
    """
    Create a list for each UPS with
    parsed metric values.
    """

    combined_metrics = []

    for conf_file in find_conf_files(conf_dir):
        ups_metrics = get_metrics(
            find_ups_nisport(conf_file)
        )

        combined_metrics.append(
            {
                "upsname": ups_metrics["UPSNAME"],
                "status": ups_metrics["STATUS"],
                "timeleft": ups_metrics["TIMELEFT"].split(" ")[0],
                "bcharge": ups_metrics["BCHARGE"].split(" ")[0],
                "loadpct": ups_metrics["LOADPCT"].split(" ")[0],
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        )

    return combined_metrics
