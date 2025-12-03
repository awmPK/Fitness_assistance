from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid
from memos.api.client import MemOSClient
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
# LangChain optional imports
LC_AVAILABLE = True
try:
    from langchain_core.messages import SystemMessage, HumanMessage
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    LC_AVAILABLE = False
import sqlite3
from datetime import datetime
# Load env from project root .env if present
_ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(_ROOT_DIR / ".env")
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MEMOS_API_KEY = os.getenv("MEMOS_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_PROVIDER_DEFAULT = os.getenv("MODEL_PROVIDER", "openai").lower()

app = FastAPI(title="Fitness AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MemoryItem(BaseModel):
    id: str
    content: str
    timestamp: str
    relevance: Optional[float] = 0.8


class ChatRequest(BaseModel):
    user_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    memory_used: bool
    related_memories: List[MemoryItem]
    conversation_id: str


class ApiResponse(BaseModel):
    success: bool
    data: Any
    message: Optional[str] = None


DB_PATH = os.path.join(os.path.dirname(__file__), 'chat.db')

def _db_connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def _db_init():
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id TEXT PRIMARY KEY,
            user_id TEXT,
            title TEXT,
            created_at TEXT,
            updated_at TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            message_id TEXT PRIMARY KEY,
            conversation_id TEXT,
            sender_type TEXT,
            content TEXT,
            timestamp TEXT
        )
        """
    )
    conn.commit()
    conn.close()

_db_init()

def _save_conversation(conversation_id: str, user_id: str, title: str):
    conn = _db_connect()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute(
        """
        INSERT INTO conversations (conversation_id, user_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(conversation_id) DO UPDATE SET title=excluded.title, updated_at=excluded.updated_at
        """,
        (conversation_id, user_id, title, now, now),
    )
    conn.commit()
    conn.close()

def _save_message(message_id: str, conversation_id: str, sender_type: str, content: str):
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO messages (message_id, conversation_id, sender_type, content, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (message_id, conversation_id, sender_type, content, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

def _get_messages(conversation_id: str) -> List[Dict[str, Any]]:
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT message_id, sender_type, content, timestamp FROM messages WHERE conversation_id=? ORDER BY timestamp ASC",
        (conversation_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {"message_id": r[0], "sender_type": r[1], "content": r[2], "timestamp": r[3]}
        for r in rows
    ]
USERS: Dict[str, Dict[str, Any]] = {}
PLANS: Dict[str, Dict[str, Any]] = {}
PROGRESS: Dict[str, Dict[str, Any]] = {}

# Initialize external clients if available
memos_client = MemOSClient(api_key=MEMOS_API_KEY) if MEMOS_API_KEY else None
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def build_system_prompt(memories: List[MemoryItem]) -> str:
    base = (
        "You are a helpful fitness assistant. Use provided memories naturally to personalize advice. "
        "Do not expose internal memory mechanisms."
    )
    if not memories:
        return base
    lines = ["## Memories:"] + [f"- {m.content}" for m in memories[:6]]
    return base + "\n" + "\n".join(lines)


def _get_langchain_llm(provider: str):
    if not LC_AVAILABLE:
        return None
    p = (provider or MODEL_PROVIDER_DEFAULT).lower()
    if p == "deepseek":
        api_key = DEEPSEEK_API_KEY
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        if not api_key:
            return None
        return ChatOpenAI(api_key=api_key, base_url=base_url, model=model, temperature=0.7)
    if p == "openai":
        api_key = OPENAI_API_KEY
        base_url = os.getenv("OPENAI_BASE_URL")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            return None
        return ChatOpenAI(api_key=api_key, base_url=base_url, model=model, temperature=0.7)
    if p == "gemini":
        api_key = GEMINI_API_KEY
        model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        if not api_key:
            return None
        return ChatGoogleGenerativeAI(api_key=api_key, model=model, temperature=0.7)
    return None


def _generate_reply_with_langchain(system_prompt: str, user_message: str, provider: str) -> Optional[str]:
    llm = _get_langchain_llm(provider)
    if not llm:
        return None
    try:
        messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_message)]
        result = llm.invoke(messages)
        return getattr(result, "content", str(result))
    except Exception:
        return None


@app.post("/api/chat/send", response_model=ApiResponse)
def send_message(req: ChatRequest):
    try:
        conv_id = req.context.get("conversation_id") if req.context else None
        if not conv_id:
            conv_id = f"conv_{uuid.uuid4().hex[:12]}"

        related: List[MemoryItem] = []

        # Search memories via MemOSClient if configured
        if memos_client:
            try:
                res = memos_client.search_memory(req.message, req.user_id, conv_id)
                for md in res.data.memory_detail_list:
                    related.append(
                        MemoryItem(
                            id=md.memory_id if hasattr(md, "memory_id") else uuid.uuid4().hex,
                            content=md.memory_value,
                            timestamp=md.updated_at if hasattr(md, "updated_at") else "",
                            relevance=0.8,
                        )
                    )
            except Exception:
                related = []

        system_prompt = build_system_prompt(related)

        # Preferred: LangChain with provider selection
        provider = (req.context or {}).get("model_provider", MODEL_PROVIDER_DEFAULT)
        reply = _generate_reply_with_langchain(system_prompt, req.message, provider)

        # Fallback: OpenAI SDK
        if not reply and openai_client:
            try:
                r = openai_client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": req.message},
                    ],
                )
                reply = r.choices[0].message.content
            except Exception:
                reply = None

        # Final fallback: deterministic text
        if not reply:
            reply = (
                "这是一个演示回复：我将根据您的健身目标提供建议。若提供了记忆，我会在训练计划与饮食建议中进行个性化引用。"
            )

        _save_conversation(conv_id, req.user_id, req.message[:20])
        _save_message(f"msg_{uuid.uuid4().hex[:10]}", conv_id, "user", req.message)
        _save_message(f"msg_{uuid.uuid4().hex[:10]}", conv_id, "assistant", reply)

        return ApiResponse(
            success=True,
            data=ChatResponse(
                reply=reply,
                memory_used=len(related) > 0,
                related_memories=related,
                conversation_id=conv_id,
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/conversation/{conversation_id}", response_model=ApiResponse)
def get_conversation(conversation_id: str):
    msgs = _get_messages(conversation_id)
    return ApiResponse(
        success=True,
        data={"conversation_id": conversation_id, "messages": msgs},
    )


@app.get("/api/chat/conversations/{user_id}", response_model=ApiResponse)
def list_conversations(user_id: str):
    conn = _db_connect()
    cur = conn.cursor()
    cur.execute("SELECT conversation_id, title FROM conversations WHERE user_id=? ORDER BY updated_at DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return ApiResponse(success=True, data=[{"conversation_id": r[0], "title": r[1] or "新对话"} for r in rows])


@app.post("/api/memos/search", response_model=ApiResponse)
def memos_search(payload: Dict[str, Any]):
    query = payload.get("query", "")
    user_id = payload.get("userId") or payload.get("user_id")
    conversation_id = payload.get("conversationId") or payload.get("conversation_id")

    items: List[MemoryItem] = []
    if memos_client and user_id:
        try:
            res = memos_client.search_memory(query, user_id, conversation_id)
            for md in res.data.memory_detail_list:
                items.append(
                    MemoryItem(
                        id=md.memory_id if hasattr(md, "memory_id") else uuid.uuid4().hex,
                        content=md.memory_value,
                        timestamp=md.updated_at if hasattr(md, "updated_at") else "",
                        relevance=0.8,
                    )
                )
        except Exception:
            items = []
    return ApiResponse(success=True, data=[m.dict() for m in items])


@app.post("/api/memos/messages", response_model=ApiResponse)
def memos_add_messages(payload: Dict[str, Any]):
    messages = payload.get("messages", [])
    user_id = payload.get("userId") or payload.get("user_id")
    conversation_id = payload.get("conversationId") or payload.get("conversation_id")
    if memos_client and user_id and conversation_id and messages:
        try:
            memos_client.add_message(messages, user_id, conversation_id)
        except Exception:
            pass
    return ApiResponse(success=True, data=None, message="messages accepted")


@app.get("/api/memos/stats/{user_id}", response_model=ApiResponse)
def memos_stats(user_id: str):
    return ApiResponse(success=True, data={"total_memories": 0, "recent_memories": 0})


# -------------------- User Endpoints --------------------
@app.get("/api/user/{user_id}", response_model=ApiResponse)
def get_user(user_id: str):
    user = USERS.get(user_id) or {
        "user_id": user_id,
        "email": "user@example.com",
        "name": "健身达人",
        "fitnessLevel": "beginner",
        "createdAt": "2025-01-01T00:00:00Z",
        "lastLoginAt": "2025-01-01T00:00:00Z",
        "height": 170,
        "weight": 65,
        "age": 25,
        "avatar": ""
    }
    USERS[user_id] = user
    return ApiResponse(success=True, data=user)


@app.put("/api/user/{user_id}", response_model=ApiResponse)
def update_user(user_id: str, payload: Dict[str, Any]):
    user = USERS.get(user_id) or {"user_id": user_id}
    user.update(payload)
    USERS[user_id] = user
    return ApiResponse(success=True, data=user)


@app.post("/api/auth/login", response_model=ApiResponse)
def login(payload: Dict[str, Any]):
    email = payload.get("email")
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    USERS[user_id] = {
        "user_id": user_id,
        "email": email,
        "name": "健身达人",
        "fitnessLevel": "beginner",
        "createdAt": "2025-01-01T00:00:00Z",
        "lastLoginAt": "2025-01-01T00:00:00Z",
    }
    return ApiResponse(success=True, data={"user": USERS[user_id], "token": f"tok_{uuid.uuid4().hex}"})


@app.post("/api/auth/register", response_model=ApiResponse)
def register(payload: Dict[str, Any]):
    email = payload.get("email")
    name = payload.get("name", "新用户")
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    USERS[user_id] = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "fitnessLevel": "beginner",
        "createdAt": "2025-01-01T00:00:00Z",
        "lastLoginAt": "2025-01-01T00:00:00Z",
    }
    return ApiResponse(success=True, data={"user": USERS[user_id], "token": f"tok_{uuid.uuid4().hex}"})


# -------------------- Plan Endpoints --------------------
@app.get("/api/plan/{user_id}", response_model=ApiResponse)
def get_user_plan(user_id: str):
    plans = [p for p in PLANS.values() if p.get("userId") == user_id]
    return ApiResponse(success=True, data=plans[0] if plans else None)


@app.post("/api/plan", response_model=ApiResponse)
def create_plan(payload: Dict[str, Any]):
    plan_id = f"plan_{uuid.uuid4().hex[:8]}"
    plan = {
        "id": plan_id,
        "userId": payload.get("userId"),
        "name": payload.get("name"),
        "description": payload.get("description", ""),
        "goal": payload.get("goal", "general"),
        "duration": payload.get("duration", 4),
        "frequency": payload.get("frequency", 3),
        "startDate": payload.get("startDate"),
        "endDate": payload.get("endDate"),
        "status": "active",
    }
    PLANS[plan_id] = plan
    return ApiResponse(success=True, data=plan)


@app.put("/api/plan/{plan_id}", response_model=ApiResponse)
def update_plan(plan_id: str, payload: Dict[str, Any]):
    plan = PLANS.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan.update(payload)
    PLANS[plan_id] = plan
    return ApiResponse(success=True, data=plan)


@app.delete("/api/plan/{plan_id}", response_model=ApiResponse)
def delete_plan(plan_id: str):
    PLANS.pop(plan_id, None)
    return ApiResponse(success=True, data=None)


# -------------------- Progress Endpoints --------------------
@app.get("/api/progress/{user_id}", response_model=ApiResponse)
def get_progress(user_id: str):
    items = [r for r in PROGRESS.values() if r.get("user_id") == user_id]
    return ApiResponse(success=True, data=items)


@app.post("/api/progress", response_model=ApiResponse)
def create_progress(payload: Dict[str, Any]):
    rid = f"rec_{uuid.uuid4().hex[:8]}"
    record = {
        "record_id": rid,
        "user_id": payload.get("user_id"),
        "workout_date": payload.get("workout_date"),
        "exercise_name": payload.get("exercise_name"),
        "sets_completed": payload.get("sets_completed", 0),
        "reps_completed": payload.get("reps_completed", 0),
        "weight_used": payload.get("weight_used", 0),
        "duration_minutes": payload.get("duration_minutes", 0),
        "calories": payload.get("calories", 0),
    }
    PROGRESS[rid] = record
    return ApiResponse(success=True, data=record)


@app.put("/api/progress/{record_id}", response_model=ApiResponse)
def update_progress(record_id: str, payload: Dict[str, Any]):
    record = PROGRESS.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    record.update(payload)
    PROGRESS[record_id] = record
    return ApiResponse(success=True, data=record)
