"""
Fully-qualified paths and other
global constants.
"""

import os
import yaml

FILE_PATH   = os.path.abspath(__file__)
SRC_DIR     = os.path.dirname(FILE_PATH)
PROJECT_DIR = os.path.dirname(SRC_DIR)

CONF_DIR    = os.path.join(PROJECT_DIR, "conf")
CONF_FILE   = os.path.join(CONF_DIR, "lazarus.yml")
DATA_DIR    = os.path.join(PROJECT_DIR, "data")
JOBS_FILE   = os.path.join(DATA_DIR, "jobs.json")

with open(CONF_FILE, "r", encoding="utf-8") as l_config:
    l_config_loaded = yaml.safe_load(l_config)["lazarus"]

INGEST_FILE = l_config_loaded["ingest_file"]

DATE_FORMAT     = l_config_loaded["format"]["date"]
TIME_FORMAT     = l_config_loaded["format"]["time"]
DATETIME_FORMAT = DATE_FORMAT + "T" + TIME_FORMAT + "Z"

ELASTIC_INGEST_INTERVAL = l_config_loaded["elastic_interval"]
JOB_EXECUTE_DELTA       = l_config_loaded["job_execute_delta"]

POWER_TRIGGER_STATUS_INTERVAL = l_config_loaded["power"]["trigger"]["status"]
POWER_TRIGGER_EVENT_INTERVAL  = l_config_loaded["power"]["trigger"]["event"]

POWER_CLEAR_STATUS_INTERVAL = l_config_loaded["power"]["clear"]["status"]
POWER_CLEAR_EVENT_INTERVAL  = l_config_loaded["power"]["clear"]["event"]
