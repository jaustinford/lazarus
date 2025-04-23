"""
Monitor UPS metric data to determine
when to execute other docker container
services on the system host.
"""

import time
import apc

APC_UPS = [
    "ups-0",
    "ups-1"
]

def find_ups_nisport(ups_name: str):
    """
    Read the conf file for a given UPS
    and return the configured NISPORT.
    """

    conf_file = "/etc/apcupsd/" + ups_name + ".conf"

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

    for apc_ups in APC_UPS:
        apc.start_daemon(apc_ups)

    while True:
        combined_metrics = []

        for apc_ups in APC_UPS:
            ups_metrics = apc.get_metrics(
                find_ups_nisport(apc_ups)
            )

            combined_metrics.append(
                {
                    apc_ups: {
                        "status": ups_metrics["STATUS"],
                        "timeleft": ups_metrics["TIMELEFT"].split(" ")[0],
                        "bcharge": ups_metrics["BCHARGE"].split(" ")[0],
                        "loadpct": ups_metrics["LOADPCT"].split(" ")[0]
                    }
                }
            )

        print(combined_metrics)

        time.sleep(10)

if __name__ == "__main__":
    main()
