"""Configuration and .env loader"""
import os
from pathlib import Path
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
# Determine safe user data directory (do NOT store user data inside installation directory)
USER_DATA_DIR = None
if os.getenv('DE_JURIST_DATA_DIR'):
    USER_DATA_DIR = Path(os.getenv('DE_JURIST_DATA_DIR'))
else:
    # Prefer APPDATA on Windows, fallback to user home .dejurist
    appdata = os.getenv('APPDATA') or os.getenv('LOCALAPPDATA')
    if appdata:
        USER_DATA_DIR = Path(appdata) / 'DE-JURIST-AI'
    else:
        USER_DATA_DIR = Path.home() / '.dejurist'

USER_DATA_DIR.mkdir(parents=True, exist_ok=True)

config = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'DE_JURIST_MODEL': os.getenv('DE_JURIST_MODEL', 'gpt-5.5'),
    'LOCAL_PROCESSING': os.getenv('DE_JURIST_LOCAL_PROCESSING', '1') in ('1','true','True'),
    'UPLOAD_OPT_IN': os.getenv('DE_JURIST_UPLOAD_OPT_IN', '0') in ('1','true','True'),
    'DATA_DIR': str(USER_DATA_DIR),
    'DB_PATH': str(USER_DATA_DIR / 'database.sqlite'),
}
