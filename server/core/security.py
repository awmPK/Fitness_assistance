"""
安全工具模块 - 密码哈希和 JWT 令牌管理
"""
import hashlib
import jwt
from datetime import timedelta
from typing import Optional, Dict, Any
from config.settings import settings
from utils.timezone import BEIJING_TZ
from datetime import datetime


def hash_password(password: str) -> str:
    """使用 SHA256 和盐值对密码进行哈希"""
    salt = "fitness_ai_salt_2025"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """验证密码是否与哈希值匹配"""
    return hash_password(password) == password_hash


def create_jwt_token(user_id: str, email: str) -> str:
    """为用户创建 JWT 令牌"""
    now = datetime.now(BEIJING_TZ)
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": now + timedelta(hours=settings.JWT_EXPIRE_HOURS),
        "iat": now
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """验证 JWT 令牌并返回载荷"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
