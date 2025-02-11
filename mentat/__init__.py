from pythonjsonlogger.json import JsonFormatter

import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
