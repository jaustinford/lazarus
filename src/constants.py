"""
Fully-qualified paths, parsed configurations
and other global variables.
"""

import os
import logging
import yaml

##################################################
# paths
##################################################

CONSTANTS_FILE = os.path.abspath(__file__)
SRC_DIR        = os.path.dirname(CONSTANTS_FILE)
PROJECT_DIR    = os.path.dirname(SRC_DIR)

CONF_DIR          = os.path.join(PROJECT_DIR, "conf")
CONF_LAZARUS_FILE = os.path.join(CONF_DIR, "lazarus.yml")
DATA_DIR          = os.path.join(PROJECT_DIR, "data")
JOBS_FILE         = os.path.join(DATA_DIR, "jobs.json")

ELASTIC_DIR           = os.path.join(PROJECT_DIR, "elastic")
ELASTIC_POLICY_FILE   = os.path.join(ELASTIC_DIR, "lifecycle_policy.json")
ELASTIC_TEMPLATE_FILE = os.path.join(ELASTIC_DIR, "index_template.json")

##################################################
# read configurations
##################################################

with open(CONF_LAZARUS_FILE, "r", encoding="utf-8") as conf_lazarus_opened:
    CONF_LAZARUS_YAML = yaml.safe_load(conf_lazarus_opened)["lazarus"]

with open(ELASTIC_POLICY_FILE, "r", encoding="utf-8") as elastic_policy_opened:
    ELASTIC_POLICY_READ = elastic_policy_opened.read()

with open(ELASTIC_TEMPLATE_FILE, "r", encoding="utf-8") as elastic_template_opened:
    ELASTIC_TEMPLATE_READ = elastic_template_opened.read()

##################################################
# logging
##################################################

LOGGING_FORMAT_BANNER = CONF_LAZARUS_YAML["logging"]["format"]["banner"]
LOGGING_FORMAT_DATE   = CONF_LAZARUS_YAML["logging"]["format"]["date"]
LOGGING_FORMAT_TIME   = CONF_LAZARUS_YAML["logging"]["format"]["time"]

logging.basicConfig(
    format=LOGGING_FORMAT_BANNER,
    datefmt=LOGGING_FORMAT_DATE + " " + LOGGING_FORMAT_TIME + " %Z",
    level=logging.INFO
)

ELASTIC_LOG = logging.getLogger("elastic_transport")
ELASTIC_LOG.setLevel(logging.CRITICAL)

##################################################
# general
##################################################

LOOP_INTERVAL = CONF_LAZARUS_YAML["loop_interval"]

INGEST_FILE = CONF_LAZARUS_YAML["ingest_file"]

DOC_FORMAT_TIMEDATE = LOGGING_FORMAT_DATE + "T" + LOGGING_FORMAT_TIME + "Z"

ELASTIC_INGEST_INTERVAL = CONF_LAZARUS_YAML["elastic_interval"]
JOB_EXECUTE_DELTA       = CONF_LAZARUS_YAML["job_execute_delta"]

POWER_TRIGGER_STATUS_INTERVAL = CONF_LAZARUS_YAML["power"]["trigger"]["status"]
POWER_TRIGGER_EVENT_INTERVAL  = CONF_LAZARUS_YAML["power"]["trigger"]["event"]

POWER_CLEAR_STATUS_INTERVAL = CONF_LAZARUS_YAML["power"]["clear"]["status"]
POWER_CLEAR_EVENT_INTERVAL  = CONF_LAZARUS_YAML["power"]["clear"]["event"]

ELASTIC_ENDPOINT = os.environ.get("ELASTIC_ENDPOINT")
VAULT_ENDPOINT   = os.environ.get("VAULT_ENDPOINT")
