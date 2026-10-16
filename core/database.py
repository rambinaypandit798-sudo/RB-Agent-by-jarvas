"""
RB.AI - Production Persistent Database Engine
Uses SQLite3 for zero-dependency, bulletproof on-device persistence of
User Profiles, Notes/Memory, Chat Histories, and Integration Configs.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_DIR = os.path.expanduser("~/rb_ai/data")
DB_PATH = os.path.join(DB_DIR, "rb_agent.db")

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. User Profile & Settings
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # 2. Notes & Memory Store (for Memory & Notes Sub-Agent)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes_memory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    created_at TEXT NOT NULL
                )
            """)

            # 3. Persistent Chat Messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender TEXT NOT NULL,
                    message TEXT NOT NULL,
                    agent_type TEXT DEFAULT 'general',
                    tool_calls TEXT DEFAULT '[]',
                    timestamp TEXT NOT NULL
                )
            """)

            # 4. Integrations Config (Telegram, GitHub, WhatsApp)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS integrations (
                    service TEXT PRIMARY KEY,
                    config_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            
            conn.commit()

        # Seed default user name if missing
        self.init_default_settings()

    def init_default_settings(self):
        default_user = "Ram Binay kumar Pandit"
        if not self.get_setting("user_name"):
            self.set_setting("user_name", default_user)
        if not self.get_setting("voice_pitch"):
            self.set_setting("voice_pitch", "1.0")
        if not self.get_setting("voice_rate"):
            self.set_setting("voice_rate", "0.9")
        if not self.get_setting("voice_accent"):
            self.set_setting("voice_accent", "hi-IN")
        if not self.get_setting("wake_phrase_enabled"):
            self.set_setting("wake_phrase_enabled", "true")
        if not self.get_setting("call_announcement_enabled"):
            self.set_setting("call_announcement_enabled", "true")
        if not self.get_setting("theme_mode"):
            self.set_setting("theme_mode", "light")

    # --- Settings Operations ---
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM user_settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row["value"] if row else default

    def set_setting(self, key: str, value: str):
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_settings (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            """, (key, str(value), now))
            conn.commit()

    def get_all_settings(self) -> Dict[str, str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM user_settings")
            return {row["key"]: row["value"] for row in cursor.fetchall()}

    # --- Notes & Memory Operations ---
    def add_note(self, title: str, content: str, tags: str = "") -> int:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notes_memory (title, content, tags, created_at)
                VALUES (?, ?, ?, ?)
            """, (title, content, tags, now))
            conn.commit()
            return cursor.lastrowid

    def get_notes(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if search:
                query = "%" + search.lower() + "%"
                cursor.execute("""
                    SELECT * FROM notes_memory
                    WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ? OR LOWER(tags) LIKE ?
                    ORDER BY id DESC
                """, (query, query, query))
            else:
                cursor.execute("SELECT * FROM notes_memory ORDER BY id DESC")
            return [dict(row) for row in cursor.fetchall()]

    def delete_note(self, note_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes_memory WHERE id = ?", (note_id,))
            conn.commit()
            return cursor.rowcount > 0

    # --- Chat History Operations ---
    def add_chat(self, sender: str, message: str, agent_type: str = "general", tool_calls: Optional[List[Any]] = None) -> int:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tc_json = json.dumps(tool_calls or [])
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history (sender, message, agent_type, tool_calls, timestamp)
                VALUES (?, ?, ?, ?, ?)
            """, (sender, message, agent_type, tc_json, now))
            conn.commit()
            return cursor.lastrowid

    def get_chats(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM chat_history ORDER BY id DESC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            chats = []
            for r in reversed(rows):
                d = dict(r)
                try:
                    d["tool_calls"] = json.loads(d["tool_calls"])
                except Exception:
                    d["tool_calls"] = []
                chats.append(d)
            return chats

    def clear_chats(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chat_history")
            conn.commit()

    # --- Integrations Operations ---
    def save_integration(self, service: str, config: Dict[str, Any]):
        now = datetime.now().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO integrations (service, config_json, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(service) DO UPDATE SET config_json = excluded.config_json, updated_at = excluded.updated_at
            """, (service, json.dumps(config), now))
            conn.commit()

    def get_integration(self, service: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT config_json FROM integrations WHERE service = ?", (service,))
            row = cursor.fetchone()
            if row:
                try:
                    return json.loads(row["config_json"])
                except Exception:
                    return {}
            return {}

# Global database instance
db = Database()
