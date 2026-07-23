import sqlite3

conn = sqlite3.connect("levels.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)
""")

conn.commit()


def get_user(user_id):
    cursor.execute(
        "SELECT xp, level FROM users WHERE user_id = ?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result:
        return result

    cursor.execute(
        "INSERT INTO users (user_id, xp, level) VALUES (?, 0, 1)",
        (user_id,)
    )

    conn.commit()

    return (0, 1)


def update_user(user_id, xp, level):
    cursor.execute(
        """
        INSERT INTO users (user_id, xp, level)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET xp=?, level=?
        """,
        (user_id, xp, level, xp, level)
    )

    conn.commit()
