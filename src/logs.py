"""
Create logging object with options.
"""

import logging

logging.basicConfig(
    format="%(asctime)s [ %(levelname)s ] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.INFO
)

ES_LOGGER = logging.getLogger("elastic_transport")
ES_LOGGER.setLevel(logging.CRITICAL)

GENERAL_LOGGER = logging.getLogger(__name__)
