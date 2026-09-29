from pydoc import doc
from tkinter import filedialog, messagebox
from tkinter import filedialog, messagebox, Menu
import customtkinter as ctk
from tkinter import ttk
from tkinter import filedialog, messagebox
from services.document_service import (
    upload_document,
    get_documents,
    search_documents,
    open_document,
    delete_document,
    get_document
)
from services.workflow_service import submit_for_approval
from gui.version_history import VersionHistoryWindow
from gui.pdf_preview import PDFPreviewWindow

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DocumentWindow(ctk.CTkToplevel):

    def __init__(self, parent, user_id):
        super().__init__(parent)

        self.user_id = user_id
        self.documents = []

        self.title("Enterprise IDWMS v2 - Document Repository")
        self.geometry("1200x760")

        self.create_ui()
        self.load_documents()

    def create_ui(self):

        ctk.CTkLabel(
            self,
            text="Document Repository",
            font=(None, 24, "bold")
        ).pack(pady=15)

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=20, pady=10)

        self.title_entry = ctk.CTkEntry(
            top,
            width=260,
            placeholder_text="Document title"
        )
        self.title_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            top,
            text="Upload",
            width=120,
            command=self.upload
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            top,
            text="Refresh",
            width=120,
            command=self.load_documents
        ).pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(
            top,
            width=260,
            placeholder_text="Search title, category, OCR text"
        )
        self.search_entry.pack(side="right", padx=10)

        ctk.CTkButton(
            top,
            text="Search",
            width=120,
            command=self.search
        ).pack(side="right")

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "title", "category", "type", "size", "date"),
            show="headings",
            height=15
    )

        self.table.heading("id", text="ID")
        self.table.heading("title", text="Title")
        self.table.heading("category", text="Category")
        self.table.heading("type", text="Type")
        self.table.heading("size", text="Size (KB)")
        self.table.heading("date", text="Upload Date")

        self.table.column("id", width=60, anchor="center")
        self.table.column("title", width=280)
        self.table.column("category", width=120, anchor="center")
        self.table.column("type", width=80, anchor="center")
        self.table.column("size", width=100, anchor="center")
        self.table.column("date", width=220)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        self.table.bind("<Double-1>", self.open_selected_document)
        self.table.bind("<Button-3>", self.show_context_menu)
        scrollbar.pack(side="right", fill="y")

        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            bottom,
            text="Open Latest",
            width=130,
            command=self.open_latest
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Preview Latest",
            width=140,
            command=self.preview_latest
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Delete Latest",
            width=140,
            fg_color="red",
            hover_color="darkred",
            command=self.delete_latest
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Submit for Approval",
            width=180,
            fg_color="green",
            hover_color="darkgreen",
            command=self.submit_latest
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            bottom,
            text="Version History",
            width=160,
            command=self.version_history
        ).pack(side="left", padx=5)
        self.context_menu = Menu(self, tearoff=0)

        self.context_menu.add_command(
            label="Open",
            command=self.open_selected_document
        )

        self.context_menu.add_command(
            label="Preview",
            command=self.preview_latest
        )

        self.context_menu.add_command(
            label="Submit for Approval",
            command=self.submit_latest
        )

        self.context_menu.add_command(
            label="Version History",
            command=self.version_history
        )

        self.context_menu.add_separator()

        self.context_menu.add_command(
            label="Delete",
            command=self.delete_latest
        )

    def upload(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Documents", "*.pdf *.docx *.png *.jpg *.jpeg *.txt")
            ]
        )

        if not file_path:
            return

        title = self.title_entry.get().strip()

        if title == "":
            messagebox.showwarning(
                "Warning",
                "Enter document title"
            )
            return

        try:
            upload_document(
                title,
                file_path,
                self.user_id
            )

            messagebox.showinfo(
                "Success",
                "Document uploaded successfully"
            )

            self.title_entry.delete(0, "end")

            self.load_documents()

        except Exception as e:
            messagebox.showerror(
                "Upload Error",
                str(e)
            )

    def load_documents(self):

        self.documents = get_documents()

        self.display(self.documents)

    def display(self, docs):

        for item in self.table.get_children():
            self.table.delete(item)

        for d in docs:

            size = round((d["file_size"] or 0) / 1024, 2)

            self.table.insert(
                "",
                "end",
                values=(
                    d["document_id"],
                    d["title"],
                    d["category"],
                    d["file_type"],
                    size,
                    d["upload_date"].strftime("%Y-%m-%d %H:%M")
                )
            )

    def search(self):

        keyword = self.search_entry.get().strip()

        if keyword == "":
            self.display(self.documents)
            return

        result = search_documents(keyword)

        self.display(result)

    def open_latest(self):

        if not self.documents:
            messagebox.showwarning(
                "Warning",
                "No document found"
            )
            return

        open_document(self.documents[0]["document_id"])

    def preview_latest(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a document first"
            )
            return

        item = self.table.item(selected[0])

        document_id = item["values"][0]

        doc = get_document(document_id)

        if not doc:
            return

        path = doc["file_path"]

        if doc["file_type"] == ".pdf":

            PDFPreviewWindow(
                self,
                path,
                doc["title"]
            )

        else:

            open_document(document_id)

        self.hide_context_menu()

    def delete_latest(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a document first"
            )
            return

        item = self.table.item(selected[0])
        document_id = item["values"][0]
        title = item["values"][1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{title}'?"
        )

        if not confirm:
            return

        delete_document(document_id)

        messagebox.showinfo(
            "Deleted",
            "Document deleted successfully"
        )

        self.load_documents()
        self.hide_context_menu()

    def submit_latest(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a document first"
            )
            return

        item = self.table.item(selected[0])
        document_id = item["values"][0]

        ok = submit_for_approval(
            document_id,
            self.user_id
        )

        if ok:

            messagebox.showinfo(
                "Success",
                "Document submitted for approval"
            )

        else:

            messagebox.showwarning(
                "Already Pending",
                "This document is already pending approval"
            )

        self.hide_context_menu()

    def version_history(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select a document first"
            )
            return

        item = self.table.item(selected[0])

        document_id = item["values"][0]
        title = item["values"][1]

        VersionHistoryWindow(
            self,
            document_id,
            title
        )

        self.hide_context_menu()

    def show_context_menu(self, event):

        item = self.table.identify_row(event.y)

        if item:

            self.table.selection_set(item)

            self.context_menu.post(
                event.x_root,
                event.y_root
            )

    def hide_context_menu(self, event=None):

        self.context_menu.place_forget()

        self.unbind("<Button-1>")

    def open_selected_document(self, event=None):

        selected = self.table.selection()

        if not selected:
            return

        item = self.table.item(selected[0])

        document_id = item["values"][0]

        open_document(document_id)

        self.hide_context_menu()