"""
Easily build and execute targeted
compose service profiles.
"""

import os
import wrappers

if os.environ.get("COMPOSE_PROFILE"):
    COMPOSE_PROFILE = os.environ.get("COMPOSE_PROFILE")

else:
    COMPOSE_PROFILE = input("\n \033[31mcompose profile\033[0m : ")

print(" ")

wrappers.compose_up(COMPOSE_PROFILE, "up --detach")

try:
    wrappers.compose_logs(COMPOSE_PROFILE)

except KeyboardInterrupt:
    wrappers.compose_down(COMPOSE_PROFILE)

else:
    wrappers.compose_down(COMPOSE_PROFILE)

if not os.environ.get("SKIP_PAUSE"):
    input("\nPress [enter] to continue... ")
