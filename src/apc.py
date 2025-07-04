"""
Parse results from the apcaccess
library and manage daemon.
"""

import os
import time
from datetime import datetime, timezone
from apcaccess import status

import constants
import logs
import elastic

def service_init():
    """
    Find available UPS configs and create
    daemonized processes for each.
    """

    for conf_file in find_conf_files(constants.CONF_DIR):
        logs.GENERAL_LOGGER.info("Starting APC daemon against conf file : %s", conf_file)

        start_daemon(conf_file)

def ensure_status_all(status_value: str, combined_metrics: list):
    """
    Return true if all status fields within
    'combined_metrics' are 'status_value'.
    """

    status_ensured = True

    for combined_metric in combined_metrics:
        metric_status = combined_metric["status"]

        if metric_status != status_value:
            status_ensured = False
            break

    return status_ensured

def ensure_status_any(status_value: str, combined_metrics: list):
    """
    Return true if any of the status fields within
    'combined_metrics' are 'status_value'.
    """

    status_ensured = False

    for combined_metric in combined_metrics:
        metric_status = combined_metric["status"]

        if metric_status == status_value:
            status_ensured = True
            break

    return status_ensured

def ingest_elastic(combined_metrics: list):
    """
    Iterate over combined UPS metrics
    and upload to Elasticsearch.
    """

    es_client = elastic.connect_elasticsearch()

    if not es_client.indices.exists(index="apcups-metric-data"):
        elastic.create_lifecycle_policy(es_client, "apcups")
        elastic.create_index_template(es_client, "apcups")
        es_client.indices.create_data_stream(name="apcups")

    for combined_metric in combined_metrics:
        es_client.index(
            index="apcups-metric-data",
            document=combined_metric
        )

    es_client.close()

def start_daemon(conf_file: str):
    """
    Start apcupsd daemon and bind a
    localhost TCP port.
    """

    os.system(
        "/sbin/apcupsd \
            -f " + conf_file
    )

    time.sleep(10)

def get_metrics(daemon_port: int):
    """
    Poll the UPS for the latest metrics,
    given the port of the daemon.
    """

    ups_metrics = status.parse(
        status.get(
            host="localhost",
            port=daemon_port
        )
    )

    return ups_metrics

def find_conf_files(conf_dir: str):
    """
    Return a list of the conf files
    presented in project conf directory.
    """

    conf_files = []

    for conf_file in os.listdir(conf_dir):
        conf_files.append(
            os.path.join(
                conf_dir,
                conf_file
            )
        )

    return conf_files

def find_ups_nisport(conf_file: str):
    """
    Read the conf file for a given UPS
    and return the configured 'NISPORT'
    value.
    """

    with open(conf_file, "r", encoding="utf-8") as conf_opened:
        conf_lines = conf_opened.readlines()

    for conf_line in conf_lines:
        if conf_line.startswith("NISPORT"):
            port_value = conf_line.split(" ")[1]
            break

    if not port_value:
        port_value = None

    return int(port_value)

def combine_metrics(conf_dir: str):
    """
    Create a list combining the metrics
    for each UPS.
    """

    combined_metrics = []

    for conf_file in find_conf_files(conf_dir):
        ups_metrics = get_metrics(
            find_ups_nisport(conf_file)
        )

        try:
            metric_timeleft = ups_metrics["TIMELEFT"].split(" ")[0]

        except KeyError:
            metric_timeleft = "0.0"

        combined_metrics.append(
            {
                "upsname": ups_metrics["UPSNAME"],
                "status": ups_metrics["STATUS"],
                "timeleft": metric_timeleft,
                "bcharge": ups_metrics["BCHARGE"].split(" ")[0],
                "loadpct": ups_metrics["LOADPCT"].split(" ")[0],
                "timestamp": datetime.now(timezone.utc).strftime(constants.DATETIME_FORMAT)
            }
        )

    return combined_metrics
