__version__ = "0.1.0"


import logging
import os


LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s %(asctime)s %(message)s",
)
