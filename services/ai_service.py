from database import get_connection

def ask_documents(question):
    conn = get_connection()
    cur = conn.cursor()

    keyword = question.lower().strip()

    cur.execute(
        """
        SELECT
            title,
            category,
            extracted_text
        FROM documents
        WHERE
            LOWER(title) LIKE %s
            OR LOWER(category) LIKE %s
            OR LOWER(COALESCE(extracted_text,'')) LIKE %s
        LIMIT 5
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    if not rows:
        return "No matching document found."

    answer = "Matching Documents:\n\n"

    for r in rows:

        answer += (
            f"Title: {r[0]}\n"
            f"Category: {r[1]}\n"
        )

        if r[2]:

            text = r[2][:300]

            answer += f"OCR Text: {text}...\n"

        answer += "\n"

    return answer