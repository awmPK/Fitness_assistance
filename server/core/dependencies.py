"""
FastAPI 依赖注入 - 认证相关依赖
"""
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import verify_jwt_token

# 安全认证方案
security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """获取当前已认证用户的依赖"""
    if not credentials:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    payload = verify_jwt_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="无效或过期的令牌")
    
    return payload


async def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict[str, Any]]:
    """可选获取当前用户的依赖（未认证时不报错）"""
    if not credentials:
        return None
    return verify_jwt_token(credentials.credentials)
