"""
Pydantic 请求/响应数据模型定义
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any


class MemoryItem(BaseModel):
    """记忆项模型"""
    id: str
    content: str
    timestamp: str
    relevance: Optional[float]


class ChatRequest(BaseModel):
    """聊天请求模型"""
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """聊天响应模型"""
    reply: str
    memory_used: bool
    related_memories: List[MemoryItem]
    conversation_id: str


class ApiResponse(BaseModel):
    """标准API响应模型"""
    success: bool
    data: Any
    message: Optional[str] = None


class RegisterRequest(BaseModel):
    """用户注册请求模型"""
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    """用户登录请求模型"""
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    """用户资料更新请求模型"""
    name: Optional[str] = None
    avatar: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    age: Optional[int] = None


class ChangePasswordRequest(BaseModel):
    """修改密码请求模型"""
    current_password: str
    new_password: str
