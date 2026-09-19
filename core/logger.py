import logging
import os

BASE = os.path.expanduser("~/ForensicOS")
LOG_DIR = os.path.join(BASE, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "forensicOS.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("ForensicOS")
