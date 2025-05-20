"""
Fully-qualified paths and other
global constants.
"""

import os

DATE_FORMAT     = "%Y-%m-%d"
TIME_FORMAT     = "%H:%M:%S"
DATETIME_FORMAT = DATE_FORMAT + "T" + TIME_FORMAT + "Z"

FILE_PATH   = os.path.abspath(__file__)
SRC_DIR     = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(SRC_DIR)

CONF_DIR    = os.path.join(PROJECT_DIR, "conf")
DATA_DIR    = os.path.join(PROJECT_DIR, "data")
INGEST_PATH = os.path.join(DATA_DIR, "ingest.csv")
JOBS_PATH   = os.path.join(DATA_DIR, "jobs.json")

ELASTIC_INGEST_INTERVAL = 10
JOB_TRIGGER_DELTA       = 60

POWER_TRIGGER_EVENT_INTERVAL  = 300
POWER_TRIGGER_STATUS_INTERVAL = 270

POWER_CLEAR_EVENT_INTERVAL  = 3600
POWER_CLEAR_STATUS_INTERVAL = 3300
