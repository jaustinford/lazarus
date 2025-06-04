"""
Ingest combined UPS metric data
into Elasticsearch.
"""

import os
from datetime import datetime
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
        )
    )

    return es_client

def create_lifecycle_policy(es_client: Elasticsearch, index_name: str):
    """
    Set up a rollover index management
    policy for the index.
    """

    es_client.ilm.put_lifecycle(
        policy=index_name + "-policy",
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

def create_index(es_client: Elasticsearch, index_name: str):
    """
    Create Elasticsearch index.
    """

    es_client.indices.create(
        index=index_name + "-" + \
            str(datetime.now().year()) + "." + \
            str(datetime.now().month()) + "." + \
            str(datetime.now().day()) + "-" + \
            "001",
        aliases={
            index_name + "-rollover": {}
        },
        settings={
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "index.lifecycle.name": index_name + "-policy"
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
