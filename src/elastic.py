"""
Ingest combined UPS metric data
into Elasticsearch.
"""

import os
from elasticsearch import Elasticsearch

ES_CLIENT = Elasticsearch(
    "http://" + os.environ.get("ELASTICSEARCH_ENDPOINT"),
    basic_auth=(
        os.environ.get("ELASTICSEARCH_USERNAME"),
        os.environ.get("ELASTICSEARCH_PASSWORD")
    )
)

def host_exists():
    """
    Return true if Elasticsearch
    endpoint is accessible.
    """

    return bool(ES_CLIENT.ping())

def index_exists(index_name: str):
    """
    Return true if the target index
    exists.
    """

    return ES_CLIENT.indices.exists(index=index_name)

def create_index(index_name: str):
    """
    Create Elasticsearch index if
    missing.
    """

    ES_CLIENT.indices.create(
        index=index_name,
        settings={
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        mappings={
            "properties": {
                "upsname": {
                    "type": "keyword"
                },
                "status": {
                    "type": "keyword"
                },
                "timeleft": {
                    "type": "integer"
                },
                "bcharge": {
                    "type": "integer"
                },
                "loadpct": {
                    "type": "integer"
                },
                "timestamp": {
                    "type": "date",
                    "format": "date_time"
                }
            }
        }
    )

def add_doc(index_name: str, doc_object: object):
    """
    Add metric data as a doc within
    an Elasticsearch index.
    """

    ES_CLIENT.index(
        index=index_name,
        document=doc_object
    )
