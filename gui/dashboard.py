import customtkinter as ctk
from tkinter import ttk
from tkinter import ttk, messagebox
from services.report_service import generate_dashboard_report
from gui.documents import DocumentWindow
from gui.workflow import WorkflowWindow
from gui.ai_chat import AIChatWindow
from gui.audit_logs import AuditLogWindow
from services.analytics_service import get_dashboard_stats

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DashboardWindow(ctk.CTk):

    def __init__(self, user_id, full_name, role):
        super().__init__()

        self.user_id = user_id
        self.full_name = full_name
        self.role = role

        self.title(f"Enterprise IDWMS v2 - {role} Dashboard")
        self.geometry("1200x760")

        self.stats = get_dashboard_stats()

        self.create_ui()

    def create_card(self, parent, title, value):

        colors = {
            "Total Documents": "#2563EB",
            "Pending": "#F59E0B",
            "Approved": "#16A34A",
            "Rejected": "#DC2626"
        }

        icons = {
            "Total Documents": "📄",
            "Pending": "⏳",
            "Approved": "✅",
            "Rejected": "❌"
        }

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=120,
            fg_color=colors.get(title, "#2563EB"),
            corner_radius=15
        )

        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text=f"{icons.get(title, '')} {title}",
            font=(None, 16, "bold"),
            text_color="white"
        ).pack(pady=(18, 5))

        ctk.CTkLabel(
            card,
            text=str(value),
            font=(None, 32, "bold"),
            text_color="white"
        ).pack()

        return card

    def create_ui(self):

        top = ctk.CTkFrame(self, height=70)
        top.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
            top,
            text="IDWMS",
            font=(None, 28, "bold")
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            top,
            text="Refresh Dashboard",
            width=150,
            command=self.refresh_dashboard
        ).pack(side="right", padx=10)
        
        ctk.CTkButton(
            top,
            text="Generate PDF Report",
            width=170,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.generate_report
        ).pack(side="right", padx=10)

        ctk.CTkLabel(
            top,
            text=f"{self.full_name} ({self.role})",
            font=(None, 16)
        ).pack(side="right", padx=10)

        stats_frame = ctk.CTkFrame(self)
        stats_frame.pack(fill="x", padx=20, pady=10)

        self.create_card(
            stats_frame,
            "Total Documents",
            self.stats["total_documents"]
        ).pack(side="left", padx=10, pady=10)

        self.create_card(
            stats_frame,
            "Pending",
            self.stats["pending_workflows"]
        ).pack(side="left", padx=10, pady=10)

        self.create_card(
            stats_frame,
            "Approved",
            self.stats["approved_workflows"]
        ).pack(side="left", padx=10, pady=10)

        self.create_card(
            stats_frame,
            "Rejected",
            self.stats["rejected_workflows"]
        ).pack(side="left", padx=10, pady=10)

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=20, pady=20)

        left = ctk.CTkFrame(body, width=300)
        left.pack(side="left", fill="y", padx=(0, 10))

        ctk.CTkLabel(
            left,
            text="Navigation",
            font=(None, 18, "bold")
        ).pack(pady=15)

        ctk.CTkButton(
            left,
            text="Document Repository",
            width=240,
            height=45,
            command=self.open_documents
        ).pack(pady=8)

        ctk.CTkButton(
            left,
            text="AI Document Assistant",
            width=240,
            height=45,
            command=self.open_ai
        ).pack(pady=8)

        if self.role in ["Admin", "Approver"]:

            ctk.CTkButton(
                left,
                text="Workflow Management",
                width=240,
                height=45,
                command=self.open_workflows
            ).pack(pady=8)

        if self.role == "Admin":

            ctk.CTkButton(
                left,
                text="Audit Logs",
                width=240,
                height=45,
                command=self.open_audit_logs
            ).pack(pady=8)

        right = ctk.CTkFrame(body)
        right.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            right,
            text="Category Statistics",
            font=(None, 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        category_frame = ctk.CTkFrame(right)
        category_frame.pack(fill="x", padx=20)

        for c in self.stats["categories"]:

            row = ctk.CTkFrame(category_frame, fg_color="transparent")
            row.pack(fill="x", pady=6)

            ctk.CTkLabel(
                row,
                text=c["category"],
                width=150,
                anchor="w",
                font=(None, 14, "bold")
            ).pack(side="left", padx=10)

            bar_bg = ctk.CTkFrame(
                row,
                fg_color="#E5E7EB",
                width=300,
                height=18,
                corner_radius=8
            )
            bar_bg.pack(side="left", padx=10)

            bar = ctk.CTkFrame(
                bar_bg,
                fg_color="#2563EB",
                width=max(20, c["count"] * 30),
                height=18,
                corner_radius=8
            )
            bar.place(x=0, y=0)

            ctk.CTkLabel(
                row,
                text=f"{c['count']} docs",
                width=80
            ).pack(side="right", padx=10)

        ctk.CTkLabel(
            right,
            text="Recent Documents",
            font=(None, 20, "bold")
        ).pack(anchor="w", padx=20, pady=(20, 10))

        recent_frame = ctk.CTkFrame(right)
        recent_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        recent_table = ttk.Treeview(
            recent_frame,
            columns=("title", "category", "date"),
            show="headings",
            height=8
        )

        recent_table.heading("title", text="Title")
        recent_table.heading("category", text="Category")
        recent_table.heading("date", text="Upload Date")

        recent_table.column("title", width=320)
        recent_table.column("category", width=120, anchor="center")
        recent_table.column("date", width=220, anchor="center")

        scroll = ttk.Scrollbar(
            recent_frame,
            orient="vertical",
            command=recent_table.yview
        )

        recent_table.configure(yscrollcommand=scroll.set)

        recent_table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for d in self.stats["recent_documents"]:
            recent_table.insert(
                "",
                "end",
                values=(
                    d["title"],
                    d["category"],
                    str(d["upload_date"])[:19]
                )
            )

    def refresh_dashboard(self):

        self.stats = get_dashboard_stats()

        for widget in self.winfo_children():
            widget.destroy()

        self.create_ui()

    def open_documents(self):
        win = DocumentWindow(self, self.user_id)
        win.focus_force()
        win.lift()
        win.grab_set()

    def open_workflows(self):
        win = WorkflowWindow(self, self.user_id)
        win.focus_force()
        win.lift()
        win.grab_set()

    def open_ai(self):
        win = AIChatWindow(self)
        win.focus_force()
        win.lift()
        win.grab_set()

    def open_audit_logs(self):
        win = AuditLogWindow(self)
        win.focus_force()
        win.lift()
        win.grab_set()
    
    def generate_report(self):
        try:
            filename = generate_dashboard_report()
            messagebox.showinfo(
                "Success",
                f"PDF report generated successfully!\n\n{filename}"
            )
        except Exception as e:
            messagebox.showerror("Report Error", str(e))

if __name__ == "__main__":
    app = DashboardWindow(1, "System Administrator", "Admin")
    app.mainloop()