# backend/app/api/history.py
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import sqlite3, time, os

router = APIRouter()

DB_DIR = "/app/data"
DB_PATH = os.path.join(DB_DIR, "history.db")

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim TEXT,
            publisher TEXT,
            title TEXT,
            url TEXT,
            rating TEXT,
            summary TEXT,
            created_at REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@router.post("/history")
def save_history(payload: Dict[str, Any]):
    try:
        required = ["claim", "publisher", "title", "url", "rating", "summary"]
        for k in required:
            if not payload.get(k):
                raise HTTPException(status_code=400, detail=f"Missing field: {k}")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO history (claim, publisher, title, url, rating, summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            payload["claim"].strip(),
            payload["publisher"].strip(),
            payload["title"].strip(),
            payload["url"].strip(),
            payload["rating"].strip(),
            payload["summary"].strip(),
            time.time()
        ))
        conn.commit()
        row_id = c.lastrowid
        conn.close()
        return {"status": "saved", "id": row_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
def list_history() -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = _dict_factory
        c = conn.cursor()
        c.execute("SELECT * FROM history ORDER BY created_at DESC")
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history/{item_id}")
def delete_history_item(item_id: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM history WHERE id = ?", (item_id,))
        conn.commit()
        deleted = c.rowcount
        conn.close()
        if deleted == 0:
            raise HTTPException(status_code=404, detail="Not found")
        return {"status": "deleted", "id": item_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history")
def clear_history():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM history")
        conn.commit()
        conn.close()
        return {"status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
