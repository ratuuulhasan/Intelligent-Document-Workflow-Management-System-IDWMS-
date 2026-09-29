from database import get_connection

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            user_id,
            username,
            full_name,
            role
        FROM users
        WHERE username=%s
        AND password=%s
        """,
        (username, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user