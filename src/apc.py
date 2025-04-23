"""
Parse results from the apcaccess
library and manage daemon.
"""

import os
import time
from apcaccess import status

def start_daemon(ups_name: str):
    """
    Start apcupsd daemon and bind a
    localhost TCP port.
    """

    os.system(
        "/sbin/apcupsd \
            -f /etc/apcupsd/" + ups_name + ".conf"
    )

    time.sleep(2)

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
