"""
健身AI助手API - 配置管理模块
"""
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# 按优先级加载环境变量文件：
# 1. config/.env（最高优先级）
# 2. 项目根目录 .env
# 3. 系统级 .env（通过 find_dotenv 查找）
_CONFIG_DIR = Path(__file__).resolve().parent
_ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(_CONFIG_DIR / ".env")  # config/.env（最高优先级）
load_dotenv(_ROOT_DIR / ".env")    # 项目根目录 .env
load_dotenv(find_dotenv())         # 系统级 .env


class Settings:
    """应用配置类，从环境变量加载配置项"""
    
    
    
    # 默认模型提供商（Deepseek），只提供模型简称即可
    MODEL_PROVIDER_DEFAULT: str = 'deepseek'
    
    # JWT 配置
    JWT_SECRET: str = os.getenv("JWT_SECRET", "fitness-ai-secret-key-2025")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 24
    
    # 数据库配置
    DB_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chat.db")
    
    # MemOS 客户端配置
    MEMOS_CLIENT_API_KEY: str = os.getenv("MEMOS_CLIENT_API_KEY", "")
    
    # LLM api key配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MEMOS_API_KEY: str = os.getenv("MEMOS_API_KEY", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    DASHSCOPE_BASE_URL: str = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")


settings = Settings()
