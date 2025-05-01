"""
Ingest combined UPS metric data
into Elasticsearch.
"""

import os
from elasticsearch import Elasticsearch

def connect_elasticsearch():
    """
    Attempt a connection to an elasticsearch
    endpoint, pass if can't connect.
    """

    es_client = Elasticsearch(
        "http://" + os.environ.get("ELASTICSEARCH_ENDPOINT"),
        basic_auth=(
            os.environ.get("ELASTICSEARCH_USERNAME"),
            os.environ.get("ELASTICSEARCH_PASSWORD")
        ),
        request_timeout=1
    )

    return es_client

def create_index(es_client: Elasticsearch, index_name: str):
    """
    Create Elasticsearch index if
    missing.
    """

    es_client.indices.create(
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
                    "type": "float"
                },
                "bcharge": {
                    "type": "float"
                },
                "loadpct": {
                    "type": "float"
                },
                "timestamp": {
                    "type": "date",
                    "format": "date_time_no_millis"
                }
            }
        }
    )
