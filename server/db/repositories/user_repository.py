"""
用户数据仓储 - 用户相关的数据库操作
"""
import uuid
from typing import Optional, Dict, Any
from db.database import db_connect
from utils.timezone import get_beijing_time
from core.security import hash_password


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """根据邮箱获取用户信息"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "user_id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "name": row[3],
        "avatar": row[4],
        "height": row[5],
        "weight": row[6],
        "age": row[7],
        "created_at": row[8],
        "updated_at": row[9],
        "last_login_at": row[10]
    }


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """根据用户ID获取用户信息"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
    
    return {
        "user_id": row[0],
        "email": row[1],
        "password_hash": row[2],
        "name": row[3],
        "avatar": row[4],
        "height": row[5],
        "weight": row[6],
        "age": row[7],
        "created_at": row[8],
        "updated_at": row[9],
        "last_login_at": row[10]
    }


def create_user(email: str, password: str, name: str) -> Dict[str, Any]:
    """创建新用户"""
    conn = db_connect()
    cur = conn.cursor()
    
    user_id = f"user_{uuid.uuid4().hex[:12]}"
    password_hash_value = hash_password(password)
    now = get_beijing_time()
    
    cur.execute("""
        INSERT INTO users (user_id, email, password_hash, name, avatar, height, weight, age, created_at, updated_at, last_login_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, email, password_hash_value, name, "", None, None, None, now, now, now))
    
    conn.commit()
    conn.close()
    
    return {
        "user_id": user_id,
        "email": email,
        "name": name,
        "avatar": "",
        "height": None,
        "weight": None,
        "age": None,
        "created_at": now,
        "updated_at": now,
        "last_login_at": now
    }


def update_user(user_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """更新用户信息"""
    conn = db_connect()
    cur = conn.cursor()
    
    # 动态构建更新语句
    update_fields = []
    values = []
    
    for field in ["name", "avatar", "height", "weight", "age"]:
        if field in data and data[field] is not None:
            update_fields.append(f"{field} = ?")
            values.append(data[field])
    
    if not update_fields:
        conn.close()
        return get_user_by_id(user_id)
    
    update_fields.append("updated_at = ?")
    values.append(get_beijing_time())
    values.append(user_id)
    
    query = f"UPDATE users SET {', '.join(update_fields)} WHERE user_id = ?"
    cur.execute(query, values)
    conn.commit()
    conn.close()
    
    return get_user_by_id(user_id)


def update_last_login(user_id: str):
    """更新用户最后登录时间"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_login_at = ? WHERE user_id = ?", 
                (get_beijing_time(), user_id))
    conn.commit()
    conn.close()


def update_user_password(user_id: str, new_password_hash: str):
    """更新用户密码哈希"""
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ?, updated_at = ? WHERE user_id = ?",
                (new_password_hash, get_beijing_time(), user_id))
    conn.commit()
    conn.close()
