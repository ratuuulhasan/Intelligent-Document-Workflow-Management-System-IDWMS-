import customtkinter as ctk
from services.version_service import get_version_history

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class VersionHistoryWindow(ctk.CTkToplevel):

    def __init__(self, parent, document_id, title):
        super().__init__(parent)

        self.document_id = document_id

        self.title(f"Version History - {title}")
        self.geometry("800x500")

        ctk.CTkLabel(
            self,
            text=f"Version History: {title}",
            font=(None, 22, "bold")
        ).pack(pady=15)

        self.table = ctk.CTkTextbox(
            self,
            width=720,
            height=360,
            font=(None, 13)
        )
        self.table.pack(padx=20, pady=10)

        ctk.CTkButton(
            self,
            text="Refresh",
            width=140,
            command=self.load_versions
        ).pack(pady=10)

        self.load_versions()

    def load_versions(self):

        versions = get_version_history(self.document_id)

        self.table.delete("1.0", "end")

        header = (
            f"{'VERSION':<10}"
            f"{'FILE NAME':<35}"
            f"{'SIZE(KB)':<12}"
            f"UPLOADED AT\n"
        )

        self.table.insert("end", header)
        self.table.insert("end", "=" * 80 + "\n")

        if not versions:

            self.table.insert(
                "end",
                "No version history found."
            )

            return

        for v in versions:

            size = round((v["file_size"] or 0) / 1024, 2)

            line = (
                f"V{v['version_no']:<9}"
                f"{v['file_name'][:33]:<35}"
                f"{size:<12}"
                f"{str(v['uploaded_at'])}\n"
            )

            self.table.insert("end", line)