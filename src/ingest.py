"""
Read job request entries as items
per line in an ingest.csv file and
create into objects for jobs.json.
"""

import os

import logs
import datafile

def create_file(file_path: str):
    """
    If ingest.csv does not exist,
    create as an empty file.
    """

    file_name = os.path.basename(file_path).split('.')[-2]

    if not os.path.isfile(file_path):
        logs.GENERAL_LOGGER.info("Creating %s", file_name + " file : " + file_path)
        with open(file_path, "w", encoding="utf-8") as file_opened:
            file_opened.write("")

def read_file(file_path: str):
    """
    Return a list of each line discovered
    with ingest.csv.
    """

    with open(file_path, "r", encoding="utf-8") as file_opened:
        file_readlines = file_opened.readlines()

    return file_readlines

def create_jobs(file_readlines: list):
    """
    Iterate over each line in ingest.csv
    and create an object for jobs.json.
    """

    ingest_job_list = []

    for file_readline in file_readlines:
        line_id   = datafile.generate_id()
        line_type = file_readline.split(",")[0]
        line_mode = file_readline.split(",")[1]
        line_date = file_readline.split(",")[2]
        line_time = file_readline.split(",")[3].rstrip("\n")

        logs.GENERAL_LOGGER.info("Ingesting job : %s", line_id)

        ingest_job_list.append(
            {
                "id": line_id,
                "type": line_type,
                "mode": line_mode,
                "trigger": {
                    "date": line_date,
                    "time": line_time
                }
            }
        )

    return ingest_job_list

def clear_file(file_path: str):
    """
    Open ingest.csv and close as an
    empty file.
    """

    with open(file_path, "w", encoding="utf-8") as file_opened:
        file_opened.write("")
