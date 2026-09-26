"""测算台会话接口。

只提供会话引导信息（系统默认卷），纯只读：
- 不写 walls 表（锁卷偏好不落墙面字段）
- 不写 calc_runs（查询会话信息不产生测算记录）
锁卷状态本身由前端内存持有，不经由此接口持久化。
"""
from fastapi import APIRouter, HTTPException

from app.repositories import rolls as rolls_repo

router = APIRouter()

DEFAULT_ROLL_NAME = "素色53"


def pick_default_roll(roll_items):
    """系统默认卷：种子"素色53"；缺失时回退到第一卷 clean 卷。"""
    clean = [r for r in roll_items if r.get("data_quality") == "clean"]
    named = next((r for r in clean if r.get("name") == DEFAULT_ROLL_NAME), None)
    return named or (clean[0] if clean else None)


@router.get("/session/bench")
def bench_session():
    """测算台会话引导：返回系统默认卷 id。"""
    default = pick_default_roll(rolls_repo.list_rolls())
    if default is None:
        raise HTTPException(404, "no clean roll available")
    return {"default_roll_id": default["id"]}
