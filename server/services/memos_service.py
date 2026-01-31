"""
MemOS 服务模块 - 处理记忆系统交互
"""
import uuid
from typing import List, Optional
from memos.api.client import MemOSClient
from config.settings import settings
from models.schemas import MemoryItem


class MemosService:
    """MemOS 记忆系统操作服务类"""
    
    _client: Optional[MemOSClient] = None
    
    @classmethod
    def get_client(cls) -> MemOSClient:
        """获取或创建 MemOS 客户端实例"""
        if cls._client is None:
            cls._client = MemOSClient(api_key=settings.MEMOS_CLIENT_API_KEY)
        return cls._client
    
    @classmethod
    def search_memory(cls, query: str, user_id: str, conversation_id: Optional[str] = None) -> List[MemoryItem]:
        """搜索用户记忆（过滤相关性低于0.5的结果）"""
        client = cls.get_client()
        items: List[MemoryItem] = []
        
        if not client or not user_id:
            return items
        
        try:
            res = client.search_memory(query, user_id, conversation_id)
            if hasattr(res, 'data') and hasattr(res.data, 'memory_detail_list'):
                for md in res.data.memory_detail_list:
                    memory_data = {
                        "memory_id": getattr(md, "memory_id", uuid.uuid4().hex),
                        "memory_value": getattr(md, "memory_value", ""),
                        "updated_at": getattr(md, "updated_at", ""),
                        "relevance": getattr(md, "relativity", 0),
                    }
                    if memory_data["relevance"] > 0.5:
                        items.append(
                            MemoryItem(
                                id=memory_data["memory_id"],
                                content=memory_data["memory_value"],
                                timestamp=memory_data["updated_at"],
                                relevance=memory_data["relevance"],
                            )
                        )
        except Exception:
            pass
        
        return items
    
    @classmethod
    def search_memory_all(cls, query: str, user_id: str, conversation_id: Optional[str] = None) -> List[MemoryItem]:
        """搜索用户所有记忆（不过滤相关性）"""
        client = cls.get_client()
        items: List[MemoryItem] = []
        
        if not client or not user_id:
            return items
        
        try:
            res = client.search_memory(query, user_id, conversation_id)
            if hasattr(res, 'data') and hasattr(res.data, 'memory_detail_list'):
                for md in res.data.memory_detail_list:
                    memory_data = {
                        "memory_id": getattr(md, "memory_id", uuid.uuid4().hex),
                        "memory_value": getattr(md, "memory_value", ""),
                        "updated_at": getattr(md, "updated_at", "")
                    }
                    items.append(
                        MemoryItem(
                            id=memory_data["memory_id"],
                            content=memory_data["memory_value"],
                            timestamp=memory_data["updated_at"],
                            relevance=0.8,
                        )
                    )
        except Exception:
            pass
        
        return items
    
    @classmethod
    def add_messages(cls, messages: List, user_id: str, conversation_id: str):
        """添加消息到记忆"""
        client = cls.get_client()
        
        if not client or not user_id or not conversation_id or not messages:
            return
        
        try:
            client.add_message(messages, user_id, conversation_id)
        except Exception:
            pass
