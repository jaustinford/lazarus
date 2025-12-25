"""
Store retrieved secrets into constants
which can be used by the rest of the
project.
"""

import infra.hvault

VAULT_TOKEN = infra.hvault.approle_login("lazarus")

ELASTICSEARCH_AUTH = infra.hvault.get_secret(VAULT_TOKEN, "containers/elasticsearch/users/elastic")
ELASTICSEARCH_USER = ELASTICSEARCH_AUTH["USERNAME"]
ELASTICSEARCH_PASS = ELASTICSEARCH_AUTH["PASSWORD"]
