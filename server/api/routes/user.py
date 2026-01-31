"""
用户相关 API 路由
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict
from models.schemas import UserUpdateRequest, ChangePasswordRequest, ApiResponse
from core.security import hash_password, verify_password
from core.dependencies import get_current_user
from db.repositories.user_repository import (
    get_user_by_id,
    update_user,
    update_user_password,
)

router = APIRouter(prefix="/api/user", tags=["user"])


@router.get("/{user_id}", response_model=ApiResponse)
def get_user(user_id: str, current_user: Dict = Depends(get_current_user)):
    """获取用户信息"""
    # 验证用户只能访问自己的数据
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="无权访问该用户信息")
    
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 移除敏感数据
    user_data = {k: v for k, v in user.items() if k != "password_hash"}
    
    return ApiResponse(success=True, data=user_data)


@router.put("/{user_id}", response_model=ApiResponse)
def update_user_info(user_id: str, req: UserUpdateRequest, current_user: Dict = Depends(get_current_user)):
    """更新用户信息"""
    # 验证用户只能更新自己的数据
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="无权修改该用户信息")
    
    update_data = req.dict(exclude_none=True)
    user = update_user(user_id, update_data)
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 移除敏感数据
    user_data = {k: v for k, v in user.items() if k != "password_hash"}
    
    return ApiResponse(success=True, data=user_data, message="更新成功")


@router.put("/{user_id}/password", response_model=ApiResponse)
def change_password(user_id: str, req: ChangePasswordRequest, current_user: Dict = Depends(get_current_user)):
    """修改用户密码"""
    # 验证用户只能修改自己的密码
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="无权修改该用户密码")
    
    # 从数据库获取用户
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 验证当前密码
    if not verify_password(req.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="当前密码错误")
    
    # 更新密码
    new_password_hash = hash_password(req.new_password)
    update_user_password(user_id, new_password_hash)
    
    return ApiResponse(success=True, data=None, message="密码修改成功")
