from database import get_connection


def log_action(user_id, action, details):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO audit_logs
        (
            user_id,
            action,
            details
        )
        VALUES (%s, %s, %s)
        """,
        (
            user_id,
            action,
            details
        )
    )

    conn.commit()
    cur.close()
    conn.close()


def get_audit_logs(limit=100):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            a.log_id,
            u.full_name,
            a.action,
            a.details,
            a.log_time
        FROM audit_logs a
        LEFT JOIN users u
        ON a.user_id = u.user_id
        ORDER BY a.log_time ASC
        LIMIT %s
        """,
        (limit,)
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data