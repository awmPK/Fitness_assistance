"""
LLM 服务模块 - 处理语言模型交互
"""
from typing import Optional, List
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from config.settings import settings
from models.schemas import MemoryItem


class LLMService:
    """LLM 操作服务类"""
    
    @staticmethod
    def build_system_prompt(memories: List[MemoryItem]) -> str:
        """构建包含记忆上下文的系统提示词"""
        base = """你是一个专业的健身助手，具备丰富的运动科学知识和个性化指导能力。你需要充分利用提供的用户记忆信息（如健身历史、偏好、身体数据等），为用户提供量身定制的健身建议、训练计划和营养指导。
请以自然、专业且富有同理心的方式与用户交流，确保建议既科学又实用。"""
        if not memories:
            return base
        lines = ["## Memories:"] + [f"- {m.content}" for m in memories[:6]]
        return base + "\n" + "\n".join(lines)
    
    @staticmethod
    def get_langchain_llm(provider: str):
        """根据提供商获取 LangChain LLM 实例"""
        p = (provider or settings.MODEL_PROVIDER_DEFAULT).lower()
        
        if "deepseek" in p:
            return ChatOpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL,
                model='deepseek-v3.2',
                temperature=0.7
            )
        elif "qwen" in p:
            return ChatOpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL,
                model='qwen-vl-max-2025-08-13',
                temperature=0.7
            )
        elif "glm" in p:
            return ChatOpenAI(
                api_key=settings.DASHSCOPE_API_KEY,
                base_url=settings.DASHSCOPE_BASE_URL,
                model='glm-4.7',
                temperature=0.7
            )
        return None
    
    @staticmethod
    def generate_reply(system_prompt: str, user_message: str, provider: str = "glm") -> Optional[str]:
        """使用指定的 LLM 提供商生成回复"""
        llm = LLMService.get_langchain_llm(provider)
        if not llm:
            return None
        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_message)]
            result = llm.invoke(messages)
            if hasattr(result, 'content'):
                return result.content
            else:
                return str(result) if result else None
        except Exception as e:
            print(f"LLM调用错误: {str(e)}")
            return None
