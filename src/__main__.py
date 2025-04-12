"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import os

def main():
    """
    Execute conditionals and trigger
    automations.
    """

    os.system("COMPOSE_PROFILE=site CYCLE_MODE=up python /iac-configure/triggers/profile.py")

if __name__ == "__main__":
    main()
