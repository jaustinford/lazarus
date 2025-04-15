"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import time

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
