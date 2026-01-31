# 健身 AI 助手

一个具备长时记忆能力的个性化健身智能助手，通过 MemOS 技术实现对话记忆存储与检索，为用户提供个性化的健身建议和计划指导。

## 功能介绍

- **智能对话**：与 AI 健身助手进行自然语言交互，获取健身建议
- **记忆系统**：基于 MemOS 的长期记忆，AI 能记住用户的健身历史和偏好
- **用户管理**：支持用户注册、登录、个人资料管理

## 项目结构

```
Fitness_assistance/
├── server/                    # 后端服务 (Python FastAPI)
│   ├── api/routes/            # API 路由
│   │   ├── auth.py            # 认证接口
│   │   ├── chat.py            # 聊天接口
│   │   ├── memos.py           # 记忆接口
│   │   └── user.py            # 用户接口
│   ├── config/                # 配置
│   │   ├── .env               # 环境变量配置文件
│   │   └── settings.py        # 配置管理
│   ├── core/                  # 核心模块
│   │   ├── dependencies.py    # 依赖注入
│   │   └── security.py        # 安全工具
│   ├── db/                    # 数据库
│   │   ├── database.py        # 数据库连接
│   │   └── repositories/      # 数据仓库
│   ├── models/                # 数据模型
│   │   └── schemas.py         # Pydantic 模型
│   ├── services/              # 业务服务
│   │   ├── llm_service.py     # LLM 调用服务
│   │   └── memos_service.py   # MemOS 服务
│   ├── main.py                # 应用入口
│   └── requirements.txt       # Python 依赖
│
├── src/                       # 前端源码 (Vue3 + TypeScript)
│   ├── components/            # 组件
│   ├── views/                 # 页面视图
│   ├── stores/                # Pinia 状态管理
│   ├── services/              # API 服务
│   ├── router/                # 路由配置
│   └── main.ts                # 入口文件
│
├── package.json               # 前端依赖
└── vite.config.ts             # Vite 配置
```

## 部署指南

### 后端部署

```bash
# 1. 进入后端目录
cd server

# 2. 创建 conda 环境
conda create -n fitness_ai python=3.11
conda activate fitness_ai

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量（见下方说明）

# 5. 启动服务
python main.py
# 或使用 uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务将运行在 `http://localhost:8000`

### 前端部署

```bash
# 确保服务器安装了npm包管理工具和nodejs
# 1. 在项目根目录安装依赖
npm install

# 2. 开发模式运行
npm run dev

# 3. 生产环境构建
npm run build
```

前端开发服务将运行在 `http://localhost:5173`

## 环境变量配置

在 `server/config/.env` 文件中配置以下变量：

```env
# JWT 密钥（可选，有默认值）
JWT_SECRET='your-jwt-secret-key'

# MemOS 客户端 API Key（必需，用于记忆系统）
# GitHub:https://github.com/MemTensor/MemOS
MEMOS_CLIENT_API_KEY='your-memos-client-api-key'

# LLM API Keys（根据使用的模型配置）
OPENAI_API_KEY='your-openai-api-key'
DEEPSEEK_API_KEY='your-deepseek-api-key'

# 阿里云 DashScope（默认使用）
# 可以免费使用qwen/deepseek/glm/kimi等国产模型100万token，申领地址：https://bailian.console.aliyun.com/cn-beijing/
DASHSCOPE_API_KEY='your-dashscope-api-key'
DASHSCOPE_BASE_URL='https://dashscope.aliyuncs.com/compatible-mode/v1'
```

### 环境变量说明

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `JWT_SECRET` | 否 | JWT 令牌加密密钥，生产环境建议自定义 |
| `MEMOS_CLIENT_API_KEY` | 是 | MemOS 记忆系统的 API Key |
| `DASHSCOPE_API_KEY` | 是* | 阿里云 DashScope API Key（默认 LLM 服务） |
| `DASHSCOPE_BASE_URL` | 否 | DashScope API 地址，有默认值 |
| `OPENAI_API_KEY` | 否 | OpenAI API Key（如使用 OpenAI 模型） |
| `DEEPSEEK_API_KEY` | 否 | DeepSeek API Key（如使用 DeepSeek 模型） |

> 注：至少配置一个 LLM API Key（推荐 `DASHSCOPE_API_KEY`）
