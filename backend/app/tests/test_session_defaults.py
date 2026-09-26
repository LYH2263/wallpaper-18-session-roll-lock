import app.db as db
from app import seed
from app.repositories import session_repo
from app.routers.session import session_defaults


def _fresh_db(monkeypatch, tmp_path):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()


def _roll_name(roll_id):
    conn = db.connect()
    try:
        return conn.execute("SELECT name FROM rolls WHERE id=?", (roll_id,)).fetchone()["name"]
    finally:
        conn.close()


def _count_runs():
    conn = db.connect()
    try:
        return conn.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]
    finally:
        conn.close()


def test_default_roll_is_seed_plain_53(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    assert _roll_name(session_repo.get_default_roll_id()) == "素色53"


def test_default_roll_falls_back_to_seed_name_without_setting(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    conn = db.connect()
    conn.execute("DELETE FROM settings WHERE key='default_roll_id'")
    conn.commit()
    conn.close()
    assert _roll_name(session_repo.get_default_roll_id()) == "素色53"


def test_session_defaults_route_is_read_only(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    payload = session_defaults()
    assert payload["default_roll_id"] == session_repo.get_default_roll_id()
    # 读取会话默认值不得产生 calc_runs 新行
    assert _count_runs() == 0


def test_walls_table_has_no_lock_or_roll_preference_columns(monkeypatch, tmp_path):
    _fresh_db(monkeypatch, tmp_path)
    conn = db.connect()
    try:
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(walls)").fetchall()]
    finally:
        conn.close()
    # 锁卷/默认卷偏好禁止落到墙面表字段
    assert not any(any(k in c for k in ("roll", "lock", "pref")) for c in cols)
