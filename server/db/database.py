"""
数据库连接与初始化模块
"""
import sqlite3
from config.settings import settings


def db_connect():
    """创建并返回数据库连接"""
    return sqlite3.connect(settings.DB_PATH, check_same_thread=False)


def db_init():
    """初始化数据库表结构"""
    conn = db_connect()
    cur = conn.cursor()
    
    # 用户表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT,
            avatar TEXT,
            height INTEGER,
            weight INTEGER,
            age INTEGER,
            created_at TEXT,
            updated_at TEXT,
            last_login_at TEXT
        )
    """)
    
    # 对话表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # 消息表
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            conversation_id TEXT,
            sender_type TEXT,
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
        )
    """)
    
    conn.commit()
    conn.close()
