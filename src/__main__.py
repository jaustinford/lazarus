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

    os.environ["SKIP_PAUSE"]      = "true"
    os.environ["COMPOSE_PROFILE"] = "ping"
    os.environ["CYCLE_MODE"]      = "up"

    os.system("python /iac-configure/triggers/profile.py")

if __name__ == "__main__":
    main()
