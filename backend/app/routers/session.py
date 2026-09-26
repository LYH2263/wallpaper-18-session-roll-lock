from fastapi import APIRouter
from app.repositories import session_repo

router = APIRouter()


@router.get("/session/defaults")
def session_defaults():
    # 会话级默认值（当前仅系统默认卷）。纯读取，不产生 calc_runs 行。
    return {"default_roll_id": session_repo.get_default_roll_id()}
