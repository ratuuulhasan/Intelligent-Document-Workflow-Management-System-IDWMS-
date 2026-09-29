from services.audit_service import log_action, get_audit_logs

log_action(
    1,
    "TEST",
    "Audit system is working"
)

logs = get_audit_logs()

for log in logs:
    print(log)