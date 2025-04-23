"""
Parse results from the apcaccess
library and manage daemon.
"""

import os
import time
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

    print("test 5")
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

    print("test 6")
    return ups_metrics
