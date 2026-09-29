import customtkinter as ctk
from tkinter import ttk, messagebox

from services.workflow_service import (
    get_pending_workflows,
    approve_workflow,
    reject_workflow,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class WorkflowWindow(ctk.CTkToplevel):

    def __init__(self, parent, user_id):
        super().__init__(parent)

        self.user_id = user_id
        self.workflows = []

        self.title("Enterprise IDWMS v2 - Workflow Management")
        self.geometry("1100x680")

        self.create_ui()
        self.load_workflows()

    def create_ui(self):

        ctk.CTkLabel(
            self,
            text="Workflow Management",
            font=(None, 26, "bold")
        ).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=10)

        self.search_entry = ctk.CTkEntry(
            top,
            width=300,
            placeholder_text="Search document title..."
        )
        self.search_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            top,
            text="Search",
            width=120,
            command=self.search_workflows
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            top,
            text="Refresh",
            width=120,
            command=self.load_workflows
        ).pack(side="right", padx=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "title", "status", "submitted"),
            show="headings",
            height=14
        )

        self.table.heading("id", text="Workflow ID")
        self.table.heading("title", text="Document Title")
        self.table.heading("status", text="Status")
        self.table.heading("submitted", text="Submitted At")

        self.table.column("id", width=100, anchor="center")
        self.table.column("title", width=420)
        self.table.column("status", width=140, anchor="center")
        self.table.column("submitted", width=220, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind("<<TreeviewSelect>>", self.show_selected_details)

        details = ctk.CTkFrame(self)
        details.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            details,
            text="Selected Workflow Details",
            font=(None, 18, "bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.details_box = ctk.CTkTextbox(
            details,
            height=120
        )
        self.details_box.pack(fill="x", padx=15, pady=(0, 10))

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=20, pady=15)

        ctk.CTkButton(
            bottom,
            text="Approve Selected",
            width=180,
            fg_color="#16A34A",
            hover_color="#15803D",
            command=self.approve_selected
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            bottom,
            text="Reject Selected",
            width=180,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.reject_selected
        ).pack(side="left", padx=8)

    def load_workflows(self):

        self.workflows = get_pending_workflows()

        for item in self.table.get_children():
            self.table.delete(item)

        for w in self.workflows:

            self.table.insert(
                "",
                "end",
                values=(
                    w["workflow_id"],
                    w["title"],
                    w["status"],
                    str(w["submitted_at"])[:19]
                )
            )

        self.details_box.delete("1.0", "end")
        self.details_box.insert(
            "1.0",
            "Select a workflow from the table to view details."
        )

    def search_workflows(self):

        keyword = self.search_entry.get().strip().lower()

        if keyword == "":
            self.load_workflows()
            return

        filtered = []

        for w in self.workflows:
            if keyword in w["title"].lower():
                filtered.append(w)

        for item in self.table.get_children():
            self.table.delete(item)

        for w in filtered:

            self.table.insert(
                "",
                "end",
                values=(
                    w["workflow_id"],
                    w["title"],
                    w["status"],
                    str(w["submitted_at"])[:19]
                )
            )

    def get_selected_workflow(self):

        selected = self.table.selection()

        if not selected:
            return None

        item = self.table.item(selected[0])

        workflow_id = item["values"][0]

        for w in self.workflows:
            if w["workflow_id"] == workflow_id:
                return w

        return None

    def show_selected_details(self, event=None):

        wf = self.get_selected_workflow()

        if not wf:
            return

        text = (
            f"Workflow ID: {wf['workflow_id']}\\n"
            f"Document Title: {wf['title']}\\n"
            f"Status: {wf['status']}\\n"
            f"Submitted At: {wf['submitted_at']}\\n\\n"
            "This workflow is waiting for approval action."
        )

        self.details_box.delete("1.0", "end")
        self.details_box.insert("1.0", text)

    def approve_selected(self):

        wf = self.get_selected_workflow()

        if not wf:

            messagebox.showwarning(
                "Warning",
                "Select a workflow first"
            )
            return

        approve_workflow(
            wf["workflow_id"],
            self.user_id
        )

        messagebox.showinfo(
            "Approved",
            "Workflow approved successfully"
        )

        self.load_workflows()

    def reject_selected(self):

        wf = self.get_selected_workflow()

        if not wf:

            messagebox.showwarning(
                "Warning",
                "Select a workflow first"
            )
            return

        reject_workflow(
            wf["workflow_id"],
            self.user_id,
            "Rejected by approver"
        )

        messagebox.showinfo(
            "Rejected",
            "Workflow rejected successfully"
        )

        self.load_workflows()