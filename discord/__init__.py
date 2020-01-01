"""Configure logging levels"""

import logging
import os

log_level = os.environ.get('LOG_LEVEL', logging.INFO)
log_format = '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'

root = logging.getLogger()
for handler in root.handlers:
    root.removeHandler(handler)

try:
    logging.basicConfig(format=log_format, level=log_level)
except Exception as err:
    logging.error(f'Invalid logging level set: {log_level}. Falling back to INFO')
    logging.basicConfig(format=log_format, level=logging.INFO)

# Suppress INFO logs for AWS commands
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)