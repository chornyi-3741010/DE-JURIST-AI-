"""Logging setup"""
import logging
import logging.handlers
from pathlib import Path
from .config import config

LOG_DIR = Path(config['DATA_DIR']) / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'dejurist.log'

logger = logging.getLogger('dej')
logger.setLevel(logging.DEBUG)
if not logger.handlers:
    fh = logging.handlers.RotatingFileHandler(str(LOG_FILE), maxBytes=5_000_000, backupCount=3, encoding='utf-8')
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)
