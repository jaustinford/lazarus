"""
Create logging object with options.
"""

import logging

logging.basicConfig(
    format="%(asctime)s [ %(levelname)s ] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.INFO
)
