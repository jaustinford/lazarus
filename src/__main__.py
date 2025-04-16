"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os
import time

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    os.system("/sbin/apcupsd -f /etc/apcupsd/ups-0.conf")
    os.system("/sbin/apcupsd -f /etc/apcupsd/ups-1.conf")

    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
