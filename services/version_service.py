from database import get_connection


def get_version_history(document_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            version_id,
            version_no,
            file_name,
            file_size,
            uploaded_at
        FROM document_versions
        WHERE document_id=%s
        ORDER BY version_no DESC
        """,
        (document_id,)
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def get_latest_version(document_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            version_no
        FROM document_versions
        WHERE document_id=%s
        ORDER BY version_no DESC
        LIMIT 1
        """,
        (document_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return row["version_no"]

    return 0


def add_new_version(
    document_id,
    file_name,
    file_path,
    file_size,
    user_id
):

    latest = get_latest_version(document_id)

    new_version = latest + 1

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO document_versions
        (
            document_id,
            version_no,
            file_name,
            file_path,
            file_size,
            uploaded_by
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)
        """,
        (
            document_id,
            new_version,
            file_name,
            file_path,
            file_size,
            user_id
        )
    )

    conn.commit()

    cur.close()
    conn.close()

    return new_version