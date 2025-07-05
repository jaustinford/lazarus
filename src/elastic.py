"""
Ingest combined UPS metric data
into Elasticsearch.
"""

import os
from elasticsearch import Elasticsearch

import logs

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
        )
    )

    return es_client

def create_lifecycle_policy(es_client: Elasticsearch, index_root_name: str):
    """
    Set up a rollover index management
    policy for the index.
    """

    logs.GENERAL_LOGGER.info("Creating Lifecycle Policy : %s", index_root_name)

    es_client.ilm.put_lifecycle(
        name=index_root_name + "-policy",
        body={
            "policy": {
                "phases": {
                    "hot": {
                        "actions": {
                            "rollover": {
                                "max_age": "30d",
                                "max_size": "50gb"
                            }
                        }
                    },
                    "delete": {
                        "min_age": "30d",
                        "actions": {
                            "delete": {}
                        }
                    }
                }
            }
        }
    )

def create_index_template(es_client: Elasticsearch, index_root_name: str):
    """
    Create Elasticsearch Index Template.
    """

    logs.GENERAL_LOGGER.info("Creating Index Template : %s", index_root_name)

    es_client.indices.put_index_template(
        name=index_root_name,
        body={
            "index_patterns": [index_root_name + "*"],
            "data_stream": {},
            "template": {
                "aliases": {
                    index_root_name + "-metric-data": {}
                },
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "index.lifecycle.name": index_root_name + "-policy",
                    "index.lifecycle.rollover_alias": index_root_name + "-metric-data"
                },
                "mappings": {
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
            }
        }
    )
