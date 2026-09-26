import os
import tempfile

# 必须在导入任何 app 模块前指向独立数据目录，避免碰开发库
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="wp-session-test-")

from app import seed  # noqa: E402
from app.db import connect  # noqa: E402
from app.routers.session import bench_session, pick_default_roll  # noqa: E402

seed.init_db()


def _calc_runs_count():
    conn = connect()
    try:
        return conn.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        conn.close()


def test_pick_default_roll_prefers_seed_plain53():
    rolls = [
        {"id": 9, "name": "大花64", "data_quality": "clean"},
        {"id": 3, "name": "素色53", "data_quality": "clean"},
    ]
    assert pick_default_roll(rolls)["id"] == 3


def test_pick_default_roll_skips_dirty_and_falls_back():
    rolls = [
        {"id": 1, "name": "素色53", "data_quality": "dirty"},
        {"id": 2, "name": "大花64", "data_quality": "clean"},
    ]
    assert pick_default_roll(rolls)["id"] == 2
    assert pick_default_roll([{"id": 5, "name": "x", "data_quality": "dirty"}]) is None


def test_bench_session_returns_seed_default_and_writes_nothing():
    before = _calc_runs_count()
    result = bench_session()
    conn = connect()
    try:
        row = conn.execute("SELECT id FROM rolls WHERE name='素色53'").fetchone()
        assert result["default_roll_id"] == row["id"]
        # 会话接口不得写墙面偏好字段，也不得产生 calc_runs 新行
        cols = [c["name"] for c in conn.execute("PRAGMA table_info(walls)").fetchall()]
        assert not any("roll" in c or "pref" in c or "lock" in c for c in cols)
    finally:
        conn.close()
    assert _calc_runs_count() == before
