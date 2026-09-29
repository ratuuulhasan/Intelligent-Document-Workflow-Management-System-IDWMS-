import customtkinter as ctk
from tkinter import ttk
from services.audit_service import get_audit_logs

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class AuditLogWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("IDWMS - Audit Logs")
        self.geometry("1150x700")

        self.logs = []

        self.create_ui()
        self.load_logs()

    def create_ui(self):

        ctk.CTkLabel(
            self,
            text="Audit Log Viewer",
            font=(None, 26, "bold")
        ).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            top,
            width=320,
            placeholder_text="Search user, action, or details..."
        )
        self.search_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            top,
            text="Search",
            width=120,
            command=self.search_logs
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            top,
            text="Refresh",
            width=120,
            command=self.load_logs
        ).pack(side="right", padx=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "user", "action", "details", "time"),
            show="headings",
            height=18
        )

        self.table.heading("id", text="Log ID")
        self.table.heading("user", text="User")
        self.table.heading("action", text="Action")
        self.table.heading("details", text="Details")
        self.table.heading("time", text="Date & Time")

        self.table.column("id", width=80, anchor="center")
        self.table.column("user", width=220)
        self.table.column("action", width=140, anchor="center")
        self.table.column("details", width=420)
        self.table.column("time", width=220, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind("<Double-1>", self.show_log_details)

        details_frame = ctk.CTkFrame(self)
        details_frame.pack(fill="x", padx=20, pady=(5, 15))

        ctk.CTkLabel(
            details_frame,
            text="Log Details",
            font=(None, 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.details_box = ctk.CTkTextbox(
            details_frame,
            height=120
        )
        self.details_box.pack(fill="x", padx=15, pady=(0, 10))

    def load_logs(self):

        self.logs = get_audit_logs()

        self.display_logs(self.logs)

    def display_logs(self, logs):

        for item in self.table.get_children():
            self.table.delete(item)

        for log in logs:

            self.table.insert(
                "",
                "end",
                values=(
                    log["log_id"],
                    log.get("full_name") or "Unknown",
                    log["action"],
                    (log.get("details") or "")[:60],
                    str(log["log_time"])[:19]
                )
            )

        self.details_box.delete("1.0", "end")
        self.details_box.insert(
            "1.0",
            "Double-click a log entry to view full details."
        )

    def search_logs(self):

        keyword = self.search_entry.get().strip().lower()

        if keyword == "":
            self.display_logs(self.logs)
            return

        filtered = []

        for log in self.logs:

            user = (log.get("full_name") or "").lower()
            action = (log.get("action") or "").lower()
            details = (log.get("details") or "").lower()

            if (
                keyword in user
                or keyword in action
                or keyword in details
            ):
                filtered.append(log)

        self.display_logs(filtered)

    def show_log_details(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(selected[0])

        log_id = item["values"][0]

        log = None

        for x in self.logs:
            if x["log_id"] == log_id:
                log = x
                break

        if not log:
            return

        text = (
            f"Log ID: {log['log_id']}\n"
            f"User: {log.get('full_name') or 'Unknown'}\n"
            f"Action: {log.get('action')}\n"
            f"Date & Time: {log.get('log_time')}\n\n"
            f"Details:\n{log.get('details') or ''}"
        )

        self.details_box.delete("1.0", "end")
        self.details_box.insert("1.0", text)