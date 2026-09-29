from database import get_connection

def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()

    stats = {}

    cur.execute("SELECT COUNT(*) AS total FROM documents")
    stats["total_documents"] = cur.fetchone()["total"]

    cur.execute(
        "SELECT COUNT(*) AS total FROM workflows WHERE status='Pending'"
    )
    stats["pending_workflows"] = cur.fetchone()["total"]

    cur.execute(
        "SELECT COUNT(*) AS total FROM workflows WHERE status='Approved'"
    )
    stats["approved_workflows"] = cur.fetchone()["total"]

    cur.execute(
        "SELECT COUNT(*) AS total FROM workflows WHERE status='Rejected'"
    )
    stats["rejected_workflows"] = cur.fetchone()["total"]

    cur.execute(
        """
        SELECT category, COUNT(*) AS count
        FROM documents
        GROUP BY category
        ORDER BY count DESC
        """
    )

    stats["categories"] = cur.fetchall()

    cur.execute(
        """
        SELECT title, category, upload_date
        FROM documents
        ORDER BY upload_date DESC
        LIMIT 5
        """
    )

    stats["recent_documents"] = cur.fetchall()

    cur.close()
    conn.close()

    return stats