"""
Wrap common Docker Compose
commands for quick execution.
"""

import os

FILE_PATH   = os.path.abspath(__file__)
DIR_FILE    = os.path.dirname(FILE_PATH)
DIR_PROJECT = os.path.dirname(DIR_FILE)
DIR_ENV     = os.path.join(DIR_PROJECT, "env")

def resolve_env_files(env_directory: str):
    """
    Create a string containing a list of
    known .env files.
    """

    env_files = ""

    for env_file in os.listdir(env_directory):
        if env_file.startswith(".env"):
            env_files += " --env-file=" + os.path.join(env_directory, env_file)

    return env_files

def compose_up(compose_profile: str, compose_method: str):
    """
    Execute Docker Compose to deploy
    profile service.
    """

    os.system(
        "docker compose" + \
            " --project-directory=" + DIR_PROJECT + \
            " --profile=" + compose_profile + \
            resolve_env_files(DIR_ENV) + \
            " " + compose_method
    )

def compose_down(compose_profile: str):
    """
    Execute Docker Compose to destroy
    profile service.
    """

    os.system(
        "docker compose" + \
            " --project-directory=" + DIR_PROJECT + \
            " --profile=" + compose_profile + \
            resolve_env_files(DIR_ENV) + \
            " down"
    )

def compose_logs(compose_profile: str):
    """
    Tail the logs of a running
    container.
    """

    os.system(
        "docker compose" + \
            " --project-directory=" + DIR_PROJECT + \
            " --profile=" + compose_profile + \
            resolve_env_files(DIR_ENV) + \
            " logs \
                --follow \
                --timestamps"
    )
