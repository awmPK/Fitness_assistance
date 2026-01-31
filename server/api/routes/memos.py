"""
MemOS 记忆相关 API 路由
"""
from fastapi import APIRouter, Depends
from typing import Dict, Any
from models.schemas import ApiResponse, MemoryItem
from core.dependencies import get_current_user
from services.memos_service import MemosService

router = APIRouter(prefix="/api/memos", tags=["memos"])


@router.post("/search", response_model=ApiResponse)
def memos_search(payload: Dict[str, Any], current_user: Dict = Depends(get_current_user)):
    """搜索记忆"""
    query = payload.get("query", "")
    user_id = payload.get("userId") or payload.get("user_id")
    conversation_id = payload.get("conversationId") or payload.get("conversation_id")

    items = MemosService.search_memory_all(query, user_id, conversation_id)
    
    data_list = [{"id": m.id, "content": m.content, "timestamp": m.timestamp, "relevance": m.relevance} for m in items]
    return ApiResponse(success=True, data=data_list)


@router.post("/messages", response_model=ApiResponse)
def memos_add_messages(payload: Dict[str, Any], current_user: Dict = Depends(get_current_user)):
    """添加消息到记忆"""
    messages = payload.get("messages", [])
    user_id = payload.get("userId") or payload.get("user_id")
    conversation_id = payload.get("conversationId") or payload.get("conversation_id")
    
    if user_id and conversation_id and messages:
        MemosService.add_messages(messages, user_id, conversation_id)
    
    return ApiResponse(success=True, data=None, message="消息已接收")


@router.get("/stats/{user_id}", response_model=ApiResponse)
def memos_stats(user_id: str, current_user: Dict = Depends(get_current_user)):
    """获取记忆统计"""
    return ApiResponse(success=True, data={"total_memories": 0, "recent_memories": 0})
