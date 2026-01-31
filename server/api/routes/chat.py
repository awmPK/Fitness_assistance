"""
聊天相关 API 路由
"""
import uuid
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
from models.schemas import ChatRequest, ChatResponse, ApiResponse, MemoryItem
from core.dependencies import get_current_user
from config.settings import settings
from db.repositories.conversation_repository import (
    save_conversation,
    save_message,
    get_messages,
    get_user_conversations,
)
from services.llm_service import LLMService
from services.memos_service import MemosService

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/send", response_model=ApiResponse)
def send_message(req: ChatRequest, current_user: Dict = Depends(get_current_user)):
    """发送聊天消息"""
    try:
        # 验证用户ID是否与当前用户匹配
        if req.user_id != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="用户ID不匹配")
        
        conv_id = req.context.get("conversation_id") if req.context else None
        if not conv_id:
            conv_id = f"conv_{uuid.uuid4().hex[:12]}"

        related: List[MemoryItem] = []

        # 通过 MemosService 搜索记忆
        try:
            related = MemosService.search_memory(req.message, req.user_id, conv_id)
        except Exception:
            related = []

        system_prompt = LLMService.build_system_prompt(related)
        provider = settings.MODEL_PROVIDER_DEFAULT
        reply = LLMService.generate_reply(system_prompt, req.message, provider)

        if not reply:
            reply = "这是一个演示回复：我将根据您的健身目标提供建议。若提供了记忆，我会在训练计划与饮食建议中进行个性化引用。"

        save_conversation(conv_id, req.user_id, req.message[:20])
        save_message(f"msg_{uuid.uuid4().hex[:10]}", conv_id, "user", req.message)
        save_message(f"msg_{uuid.uuid4().hex[:10]}", conv_id, "assistant", reply)

        return ApiResponse(
            success=True,
            data=ChatResponse(
                reply=reply,
                memory_used=len(related) > 0,
                related_memories=related,
                conversation_id=conv_id,
            ),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}", response_model=ApiResponse)
def get_conversation(conversation_id: str, current_user: Dict = Depends(get_current_user)):
    """获取对话历史"""
    msgs = get_messages(conversation_id)
    return ApiResponse(
        success=True,
        data={"conversation_id": conversation_id, "messages": msgs},
    )


@router.get("/conversations/{user_id}", response_model=ApiResponse)
def list_conversations(user_id: str, current_user: Dict = Depends(get_current_user)):
    """获取用户的对话列表"""
    # 验证用户只能访问自己的对话
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="无权访问该用户的对话")
    
    conversations = get_user_conversations(user_id)
    return ApiResponse(success=True, data=conversations)
