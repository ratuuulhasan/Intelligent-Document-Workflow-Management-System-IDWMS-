from database import get_connection
from services.audit_service import log_action


def submit_for_approval(document_id, submitted_by, assigned_to=3):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT workflow_id
        FROM workflows
        WHERE document_id=%s
        AND status='Pending'
        """,
        (document_id,)
    )

    existing = cur.fetchone()

    if existing:
        cur.close()
        conn.close()
        return False

    cur.execute(
        """
        INSERT INTO workflows
        (
            document_id,
            submitted_by,
            assigned_to,
            status
        )
        VALUES
        (%s,%s,%s,'Pending')
        RETURNING workflow_id
        """,
        (
            document_id,
            submitted_by,
            assigned_to
        )
    )

    workflow = cur.fetchone()
    workflow_id = workflow["workflow_id"]

    cur.execute(
        """
        INSERT INTO workflow_history
        (
            workflow_id,
            action,
            action_by,
            remarks
        )
        VALUES
        (%s,'Submitted',%s,'Document submitted for approval')
        """,
        (
            workflow_id,
            submitted_by
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    log_action(
        submitted_by,
        "WORKFLOW_SUBMITTED",
        f"Submitted document ID {document_id} for approval"
    )

    return True


def get_pending_workflows():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            w.workflow_id,
            d.title,
            w.status,
            w.submitted_at
        FROM workflows w
        JOIN documents d
        ON w.document_id=d.document_id
        WHERE w.status='Pending'
        ORDER BY w.submitted_at DESC
        """
    )

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data


def approve_workflow(workflow_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE workflows
        SET
            status='Approved',
            completed_at=CURRENT_TIMESTAMP
        WHERE workflow_id=%s
        """,
        (workflow_id,)
    )

    cur.execute(
        """
        INSERT INTO workflow_history
        (
            workflow_id,
            action,
            action_by,
            remarks
        )
        VALUES
        (%s,'Approved',%s,'Workflow approved')
        """,
        (
            workflow_id,
            user_id
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    log_action(
        user_id,
        "WORKFLOW_APPROVED",
        f"Approved workflow ID {workflow_id}"
    )


def reject_workflow(workflow_id, user_id, remarks='Rejected'):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE workflows
        SET
            status='Rejected',
            remarks=%s,
            completed_at=CURRENT_TIMESTAMP
        WHERE workflow_id=%s
        """,
        (
            remarks,
            workflow_id
        )
    )

    cur.execute(
        """
        INSERT INTO workflow_history
        (
            workflow_id,
            action,
            action_by,
            remarks
        )
        VALUES
        (%s,'Rejected',%s,%s)
        """,
        (
            workflow_id,
            user_id,
            remarks
        )
    )

    conn.commit()
    cur.close()
    conn.close()

    log_action(
        user_id,
        "WORKFLOW_REJECTED",
        f"Rejected workflow ID {workflow_id}"
    )