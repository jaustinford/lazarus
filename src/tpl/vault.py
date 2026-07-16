"""
Interact with HashiCorp Vault to retrieve
authorized secrets using the AppRole
authentication method.
"""

import json
import hvac

import constants

def read_approle(approle_file: str):
    """
    Read the AppRole credentials from a
    local file and return as a JSON
    object.
    """

    with open("/approle/" + approle_file, "r", encoding="utf-8") as approle_opened:
        approle_read = approle_opened.read()
        approle_json = json.loads(approle_read)

    return approle_json

def approle_login(approle_name: str):
    """
    Login to AppRole in Vault using
    retrieved 'role_id' and 'secret_id'
    fields provided in /approle, mounted
    from /root/approle on the host.
    """

    vault_unauth_client = hvac.Client(url=constants.VAULT_ENDPOINT)
    approle_credentials = read_approle(approle_name + ".json")

    client_token = vault_unauth_client.auth.approle.login(
        role_id=approle_credentials["role_id"],
        secret_id=approle_credentials["secret_id"]
    )["auth"]["client_token"]

    return client_token

def get_secret(vault_token: str, secret_path: str):
    """
    Use generated AppRole 'vault_token'
    to access 'secret_path' and return
    the data field.
    """

    vault_auth_client = hvac.Client(
        url=constants.VAULT_ENDPOINT,
        token=vault_token
    )

    secret_version = vault_auth_client.secrets.kv.v2.read_secret_version(
        mount_point="lab/kv",
        path=secret_path,
        raise_on_deleted_version=True
    )

    return secret_version["data"]["data"]
