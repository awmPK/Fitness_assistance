"""
对话数据仓储 - 对话和消息相关的数据库操作
"""
from typing import List, Dict, Any
from db.database import db_connect
from utils.timezone import get_beijing_time


def save_conversation(conversation_id: str, user_id: str, title: str):
    """保存或更新对话"""
    conn = db_connect()
    cur = conn.cursor()
    now = get_beijing_time()
    cur.execute("""
        INSERT INTO conversations (conversation_id, user_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(conversation_id) DO UPDATE SET title=excluded.title, updated_at=excluded.updated_at
    """, (conversation_id, user_id, title, now, now))
    conn.commit()
    conn.close()


def save_message(message_id: str, conversation_id: str, sender_type: str, content: str):
    """保存消息到对话"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages (message_id, conversation_id, sender_type, content, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (message_id, conversation_id, sender_type, content, get_beijing_time()))
    conn.commit()
    conn.close()


def get_messages(conversation_id: str) -> List[Dict[str, Any]]:
    """获取对话的所有消息"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT message_id, sender_type, content, timestamp FROM messages WHERE conversation_id=? ORDER BY timestamp ASC",
        (conversation_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"message_id": r[0], "sender_type": r[1], "content": r[2], "timestamp": r[3]}
        for r in rows
    ]


def get_user_conversations(user_id: str) -> List[Dict[str, Any]]:
    """获取用户的所有对话"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT conversation_id, title, created_at, updated_at FROM conversations WHERE user_id=? ORDER BY updated_at DESC",
        (user_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"conversation_id": r[0], "title": r[1] or "新对话", "created_at": r[2], "updated_at": r[3]}
        for r in rows
    ]
