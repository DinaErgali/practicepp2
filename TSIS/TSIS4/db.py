import psycopg2
from config import DB_CONFIG


def get_conn():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG.get("port", "5432"),
            client_encoding="UTF8"   # ⭐ 防编码错误
        )
        return conn
    except Exception as e:
        print("DB CONNECT ERROR:", e)
        return None


# 获取或创建用户
def get_player_id(username):
    conn = get_conn()
    if not conn:
        return None

    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    r = cur.fetchone()

    if r:
        pid = r[0]
    else:
        cur.execute(
            "INSERT INTO players(username) VALUES(%s) RETURNING id",
            (username,)
        )
        pid = cur.fetchone()[0]
        conn.commit()

    conn.close()
    return pid


# 保存成绩
def save_score(username, score, level):
    conn = get_conn()
    if not conn:
        return

    pid = get_player_id(username)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO game_sessions(player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (pid, score, level)
    )

    conn.commit()
    conn.close()


# 获取 Top10
def get_top10():
    conn = get_conn()
    if not conn:
        return []

    cur = conn.cursor()

    cur.execute("""
        SELECT p.username, g.score, g.level_reached
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        ORDER BY g.score DESC
        LIMIT 10
    """)

    rows = cur.fetchall()
    conn.close()
    return rows


# 获取个人最高分
def get_best(username):
    conn = get_conn()
    if not conn:
        return 0

    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(MAX(g.score), 0)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username=%s
    """, (username,))

    best = cur.fetchone()[0]

    conn.close()
    return best