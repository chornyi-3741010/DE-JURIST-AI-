"""Configuration and .env loader"""
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

config = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'DE_JURIST_MODEL': os.getenv('DE_JURIST_MODEL', 'gpt-5.5'),
    'LOCAL_PROCESSING': os.getenv('DE_JURIST_LOCAL_PROCESSING', '1') in ('1','true','True'),
    'UPLOAD_OPT_IN': os.getenv('DE_JURIST_UPLOAD_OPT_IN', '0') in ('1','true','True'),
    'DATA_DIR': str(DATA_DIR),
    'DB_PATH': str(DATA_DIR / 'database.sqlite'),
}
