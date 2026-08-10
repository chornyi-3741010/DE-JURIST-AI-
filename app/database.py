"""Database layer using sqlite3"""
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from .config import config
from .logger import logger

DB_PATH = Path(config['DB_PATH'])
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    return sqlite3.connect(str(DB_PATH), check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        filename TEXT,
        type TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS deadlines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        date TEXT,
        description TEXT,
        status TEXT DEFAULT 'open',
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        role TEXT,
        content TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()
    logger.info('Database initialized at %s', DB_PATH)

# helper functions

def create_case(title: str) -> int:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('INSERT INTO cases (title) VALUES (?)', (title,))
    conn.commit(); cid = cur.lastrowid; conn.close()
    logger.info('Created case %s', cid)
    return cid

def list_cases() -> List[Dict[str,Any]]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id, title, created, updated FROM cases ORDER BY updated DESC')
    rows = cur.fetchall(); conn.close()
    return [{'id':r[0],'title':r[1],'created':r[2],'updated':r[3]} for r in rows]

def add_document(case_id:int, filename:str, dtype:str) -> int:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('INSERT INTO documents (case_id, filename, type) VALUES (?,?,?)', (case_id, filename, dtype))
    conn.commit(); did = cur.lastrowid; conn.close()
    logger.info('Added document %s to case %s', filename, case_id)
    return did

def list_documents(case_id:int) -> List[Dict[str,Any]]:
    conn = get_conn(); cur = conn.cursor()
    cur.execute('SELECT id, filename, type, created FROM documents WHERE case_id=?', (case_id,))
    rows = cur.fetchall(); conn.close()
    return [{'id':r[0],'filename':r[1],'type':r[2],'created':r[3]} for r in rows]

def save_message(case_id:int, role:str, content:str):
    conn = get_conn(); cur = conn.cursor()
    cur.execute('INSERT INTO messages (case_id, role, content) VALUES (?,?,?)', (case_id, role, content))
    conn.commit(); conn.close()
    logger.debug('Saved message for case %s', case_id)
