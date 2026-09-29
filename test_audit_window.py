import customtkinter as ctk
from gui.audit_logs import AuditLogWindow

root = ctk.CTk()
root.withdraw()

AuditLogWindow(root)

root.mainloop()