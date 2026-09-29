import os
import shutil
from database import get_connection
from services.ocr_service import extract_text
from services.classification_service import classify_document
from services.version_service import add_new_version
from services.audit_service import log_action

UPLOAD_FOLDER = "storage/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def upload_document(title, source_path, user_id):
    file_name = os.path.basename(source_path)
    destination = os.path.join(UPLOAD_FOLDER, file_name)

    shutil.copy2(source_path, destination)

    file_size = os.path.getsize(destination)
    file_type = os.path.splitext(file_name)[1].lower()

    extracted_text = ""

    if file_type in [".png", ".jpg", ".jpeg"]:
        try:
            extracted_text = extract_text(destination)
        except Exception:
            extracted_text = ""

    category = classify_document(extracted_text)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT document_id FROM documents WHERE title=%s",
        (title,)
    )

    existing = cur.fetchone()

    if existing:

        document_id = existing["document_id"]

        cur.execute(
            """
            UPDATE documents
            SET
                file_name=%s,
                file_path=%s,
                file_size=%s,
                file_type=%s,
                category=%s,
                extracted_text=%s,
                upload_date=CURRENT_TIMESTAMP
            WHERE document_id=%s
            """,
            (
                file_name,
                destination,
                file_size,
                file_type,
                category,
                extracted_text,
                document_id
            )
        )

        conn.commit()
        cur.close()
        conn.close()

        add_new_version(
            document_id,
            file_name,
            destination,
            file_size,
            user_id
        )

        log_action(
            user_id,
            "DOCUMENT_UPDATED",
            f"Updated document: {title}"
        )

        return document_id

    cur.execute(
        """
        INSERT INTO documents
        (
            title,
            file_name,
            file_path,
            file_size,
            file_type,
            category,
            extracted_text,
            uploaded_by
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING document_id
        """,
        (
            title,
            file_name,
            destination,
            file_size,
            file_type,
            category,
            extracted_text,
            user_id
        )
    )

    document = cur.fetchone()
    document_id = document["document_id"]

    conn.commit()
    cur.close()
    conn.close()

    add_new_version(
        document_id,
        file_name,
        destination,
        file_size,
        user_id
    )

    log_action(
        user_id,
        "DOCUMENT_UPLOADED",
        f"Uploaded document: {title}"
    )

    return document_id


def get_documents():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            document_id,
            title,
            category,
            file_type,
            file_size,
            upload_date
        FROM documents
        ORDER BY document_id ASC
        """
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def search_documents(keyword):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            document_id,
            title,
            category,
            file_type,
            file_size,
            upload_date
        FROM documents
        WHERE
            LOWER(title) LIKE LOWER(%s)
            OR LOWER(category) LIKE LOWER(%s)
            OR LOWER(COALESCE(extracted_text,'')) LIKE LOWER(%s)
        ORDER BY upload_date DESC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def get_document(document_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM documents WHERE document_id=%s",
        (document_id,)
    )

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data


def delete_document(document_id, user_id=None):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT title, file_path FROM documents WHERE document_id=%s",
        (document_id,)
    )

    row = cur.fetchone()

    if row:

        title = row["title"]
        path = row["file_path"]

        if os.path.exists(path):
            os.remove(path)

        if user_id is not None:
            log_action(
                user_id,
                "DOCUMENT_DELETED",
                f"Deleted document: {title}"
            )

    cur.execute(
        "DELETE FROM documents WHERE document_id=%s",
        (document_id,)
    )

    conn.commit()
    cur.close()
    conn.close()


def open_document(document_id):
    doc = get_document(document_id)

    if not doc:
        return

    path = doc["file_path"]

    if os.path.exists(path):
        os.startfile(path)