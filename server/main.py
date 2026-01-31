"""
健身AI助手API - 应用程序入口

FastAPI 应用程序的主入口文件。
所有路由按模块组织在 api/routes/ 目录下。
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 导入数据库模块
from db.database import db_init

# 导入路由模块
from api.routes import auth, user, chat, memos

# 初始化数据库表
db_init()

# 创建 FastAPI 应用实例
app = FastAPI(title="Fitness AI Assistant API")

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册 API 路由
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(memos.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
