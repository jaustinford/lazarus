"""
Create resources required for Elastic
stack ingestion and uploading data.
"""

import os
from elasticsearch import Elasticsearch

import constants
import tpl.vault

MAIN_LOG = constants.logging.getLogger(__name__)

def create_client(index_root_name: str):
    """
    Resolve Elastic secrets and create
    connection object.
    """

    if not os.environ.get("ELASTIC_USERNAME") or not os.environ.get("ELASTIC_PASSWORD"):
        vault_token = tpl.vault.approle_login(index_root_name)

        elastic_auth = tpl.vault.get_secret(
            vault_token,
            "containers/elasticsearch/users/elastic"
        )

        os.environ["ELASTIC_USERNAME"] = elastic_auth["USERNAME"]
        os.environ["ELASTIC_PASSWORD"] = elastic_auth["PASSWORD"]

    es_client = Elasticsearch(
        constants.ELASTIC_ENDPOINT,
        basic_auth=(
            os.environ.get("ELASTIC_USERNAME"),
            os.environ.get("ELASTIC_PASSWORD")
        )
    )

    initialize_index(es_client, index_root_name)

    return es_client

def initialize_index(es_client: Elasticsearch, index_root_name: str):
    """
    Create Elastic Index resources if
    'index_root_name + "-metric-data"'
    does not exist.
    """

    if not es_client.indices.exists(index=index_root_name + "-metric-data"):
        create_lifecycle_policy(es_client, index_root_name)
        create_index_template(es_client, index_root_name)
        es_client.indices.create_data_stream(name=index_root_name)

def create_lifecycle_policy(es_client: Elasticsearch, index_root_name: str):
    """
    Create Elastic Lifecycle Policy.
    """

    es_client.ilm.put_lifecycle(
        name=index_root_name + "-policy",
        body=constants.ELASTIC_POLICY_READ
    )

    MAIN_LOG.info("Created Lifecycle Policy : %s", index_root_name)

def create_index_template(es_client: Elasticsearch, index_root_name: str):
    """
    Create Elastic Index Template.
    """

    es_client.indices.put_index_template(
        name=index_root_name,
        body=constants.ELASTIC_TEMPLATE_READ
    )

    MAIN_LOG.info("Created Index Template : %s", index_root_name)

def upload_document(es_client: Elasticsearch, index_root_name: str, index_document: object):
    """
    Upload document to Elastic.
    """

    es_client.index(
        index=index_root_name,
        document=index_document
    )

    MAIN_LOG.info("Uploaded Elastic Document : %s", index_document)
