"""
认证相关 API 路由
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from models.schemas import RegisterRequest, LoginRequest, ApiResponse
from core.security import create_jwt_token, verify_password
from core.dependencies import get_current_user
from db.repositories.user_repository import (
    get_user_by_email,
    get_user_by_id,
    create_user,
    update_last_login,
)
from utils.timezone import get_beijing_time

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=ApiResponse)
def register(req: RegisterRequest):
    """用户注册接口"""
    # 检查邮箱是否已存在
    existing_user = get_user_by_email(req.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="该邮箱已被注册")
    
    # 创建用户
    user = create_user(req.email, req.password, req.name)
    
    # 生成 JWT 令牌
    token = create_jwt_token(user["user_id"], user["email"])
    
    # 移除敏感数据
    user_data = {k: v for k, v in user.items() if k != "password_hash"}
    
    return ApiResponse(
        success=True,
        data={"user": user_data, "token": token},
        message="注册成功"
    )


@router.post("/login", response_model=ApiResponse)
def login(req: LoginRequest):
    """用户登录接口"""
    # 根据邮箱查找用户
    user = get_user_by_email(req.email)
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    # 验证密码
    if not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    # 更新最后登录时间
    update_last_login(user["user_id"])
    
    # 生成 JWT 令牌
    token = create_jwt_token(user["user_id"], user["email"])
    
    # 移除敏感数据
    user_data = {k: v for k, v in user.items() if k != "password_hash"}
    user_data["last_login_at"] = get_beijing_time()
    
    return ApiResponse(
        success=True,
        data={"user": user_data, "token": token},
        message="登录成功"
    )


@router.get("/me", response_model=ApiResponse)
def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """获取当前登录用户信息"""
    user = get_user_by_id(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 移除敏感数据
    user_data = {k: v for k, v in user.items() if k != "password_hash"}
    
    return ApiResponse(success=True, data=user_data)
