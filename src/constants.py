"""
Collection of shared constants.
"""

import os

TIME_FORMAT_TIMESTAMP = "%Y-%m-%dT%H:%M:%SZ"
TIME_FORMAT_CYCLE     = "%Y-%m-%d %H:%M"

FILE_PATH   = os.path.abspath(__file__)
SRC_DIR     = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(SRC_DIR)

CONF_DIR         = os.path.join(PROJECT_DIR, "conf")
DATA_DIR         = os.path.join(PROJECT_DIR, "data")
CYCLES_PATH      = os.path.join(PROJECT_DIR, DATA_DIR, "cycles.json")
CYCLES_LOCK_PATH = os.path.join(PROJECT_DIR, DATA_DIR, "cycles.lock")
HISTORY_PATH     = os.path.join(PROJECT_DIR, DATA_DIR, ".history.json")

MONTHS = {
    "01": 31, "02": 28, "03": 31, "04": 30,
    "05": 31, "06": 30, "07": 31, "08": 31, 
    "09": 30, "10": 31, "11": 30, "12": 31
}
