from app.db import connect

DEFAULT_ROLL_NAME = "素色53"


def get_default_roll_id():
    """系统默认卷 id：settings.default_roll_id 优先，其次种子素色53，再退到首条干净卷。

    只读查询——会话默认值不落墙面表，也绝不写 calc_runs。
    """
    conn = connect()
    try:
        row = conn.execute("SELECT value FROM settings WHERE key='default_roll_id'").fetchone()
        if row:
            rid = int(row["value"])
            ok = conn.execute(
                "SELECT 1 FROM rolls WHERE id=? AND data_quality='clean'", (rid,)
            ).fetchone()
            if ok:
                return rid
        row = conn.execute(
            "SELECT id FROM rolls WHERE name=? AND data_quality='clean' ORDER BY id LIMIT 1",
            (DEFAULT_ROLL_NAME,),
        ).fetchone()
        if row:
            return int(row["id"])
        row = conn.execute(
            "SELECT id FROM rolls WHERE data_quality='clean' ORDER BY id LIMIT 1"
        ).fetchone()
        return int(row["id"]) if row else None
    finally:
        conn.close()
