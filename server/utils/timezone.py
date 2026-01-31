"""
时区工具模块
"""
from datetime import datetime, timedelta, timezone

# 北京时区（UTC+8）
BEIJING_TZ = timezone(timedelta(hours=8))


def get_beijing_time() -> str:
    """获取当前北京时间，返回 ISO 格式字符串"""
    return datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S")
