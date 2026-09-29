import customtkinter as ctk
from services.pdf_ai_service import extract_text_from_pdf
from database import get_connection



class AIChatWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("Enterprise IDWMS v2 - AI Document Assistant")
        self.geometry("950x700")

        ctk.CTkLabel(
            self,
            text="AI Document Assistant",
            font=ctk.CTkFont(size=28, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text="Ask questions about your documents (ChatGPT-style)",
            font=ctk.CTkFont(size=14)
        ).pack()

        self.chat_box = ctk.CTkTextbox(self, width=860, height=420)
        self.chat_box._textbox.configure(wrap="word")
        self.chat_box.pack(padx=20, pady=20)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)

        self.question_entry = ctk.CTkEntry(
            input_frame,
            width=650,
            placeholder_text="Ask about your documents..."
        )
        self.question_entry.pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            input_frame,
            text="Ask AI",
            command=self.process_question,
            width=150
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            self,
            text="Load Latest Document",
            command=self.load_latest_document,
            width=220
        ).pack(pady=10)

        self.show_welcome()

    def show_welcome(self):
        welcome = """Welcome to Enterprise IDWMS AI Assistant

You can ask:

• Find all NID documents
• Find passport documents
• Summarize latest document
• Suggest workflow
• Show recent documents
• Help

This AI assistant searches your enterprise document repository and provides intelligent responses.
"""

        self.chat_box.delete("1.0", "end")
        self.chat_box.insert("end", welcome)

    def add_message(self, sender, message):
        # Fix newline formatting
        message = message.replace("\\\\n", "\n")

        if sender == "You":
            self.chat_box.insert(
                "end",
                "\n" + " " * 35 + "YOU\n",
                "you"
            )
            self.chat_box.insert(
                "end",
                " " * 20 + message + "\n",
                "you_msg"
            )
        else:
            self.chat_box.insert(
                "end",
                "\nAI ASSISTANT\n",
                "ai"
            )
            self.chat_box.insert(
                "end",
                message + "\n",
                "ai_msg"
            )

        self.chat_box.insert("end", "\n" + "─" * 70 + "\n")
        self.chat_box.see("end")

        # Text styling
        self.chat_box.tag_config("you", justify="right")
        self.chat_box.tag_config("you_msg", justify="right")
        self.chat_box.tag_config("ai", justify="left")
        self.chat_box.tag_config("ai_msg", justify="left")

    def process_question(self):
        question = self.question_entry.get().strip()

        if not question:
            return

        self.add_message("You", question)

        q = question.lower()

        if "nid" in q:
            response = self.find_documents_by_category("NID")

        elif "passport" in q:
            response = self.find_documents_by_category("Passport")

        elif "invoice" in q:
            response = self.find_documents_by_category("Invoice")

        elif "summarize" in q or "summary" in q:
            response = self.summarize_latest_document()

        elif "name" in q or "applicant" in q:
            response = self.extract_document_information("name")

        elif "nid number" in q or "nid no" in q:
            response = self.extract_document_information("nid")

        elif "passport number" in q:
            response = self.extract_document_information("passport")

        elif "expiry" in q or "expire" in q:
            response = self.extract_document_information("expiry")

        elif "amount" in q or "invoice amount" in q:
            response = self.extract_document_information("amount")

        elif "approval" in q or "approve" in q:
            response = self.extract_document_information("approval")

        elif "workflow" in q:
            response = self.workflow_recommendation()

        elif "recent" in q:
            response = self.show_recent_documents()

        elif "help" in q:
            response = """
Available AI commands:

- Find all NID documents
- Find passport documents
- Find invoice documents
- Summarize latest document
- Suggest workflow
- Show recent documents
- Help
"""

        else:
            response = "I can help you search documents, summarize the latest document, suggest workflows, and find documents by category."

        self.add_message("AI Assistant", response)

        self.question_entry.delete(0, "end")

    def find_documents_by_category(self, category):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT title, category, upload_date
                FROM documents
                WHERE category = %s
                ORDER BY upload_date DESC
                LIMIT 10
                """,
                (category,)
            )

            rows = cur.fetchall()

            cur.close()
            conn.close()

            if not rows:
                return f"No {category} documents found in the repository."

            lines = [f"Found {len(rows)} {category} document(s):", ""]

            for row in rows:
                if isinstance(row, dict):
                    title = row.get("title", "Untitled")
                    upload = row.get("upload_date", "Unknown")
                else:
                    title = row[0]
                    upload = row[2]

                lines.append(f"• {title}")
                lines.append(f"  Uploaded: {upload}")
                lines.append("")

            return "\n".join(lines)

        except Exception as e:
            return f"Search failed: {str(e)}"

    def summarize_latest_document(self):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT title, category
                FROM documents
                ORDER BY upload_date DESC
                LIMIT 1
                """
            )

            row = cur.fetchone()

            cur.close()
            conn.close()

            if not row:
                return "No documents found in the repository."

            if isinstance(row, dict):
                title = row.get("title", "Untitled")
                category = row.get("category", "Other")
            else:
                title = row[0]
                category = row[1]

            return f"""
Latest document summary

Title: {title}
Category: {category}

AI Summary:
This is the most recently uploaded document in the Enterprise IDWMS repository. The document has been classified under the {category} category and is ready for workflow processing, approval, and secure archival.
"""

        except Exception as e:
            return f"Summary failed: {str(e)}"

    def workflow_recommendation(self):
        return """
Recommended enterprise workflow

1. Document Upload
2. AI Classification
3. Admin Verification
4. Approval Workflow
5. Audit Logging
6. Secure Archive

This workflow ensures compliance, traceability, and secure document management.
"""

    def show_recent_documents(self):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
                """
                SELECT title, category
                FROM documents
                ORDER BY upload_date DESC
                LIMIT 5
                """
            )

            rows = cur.fetchall()

            cur.close()
            conn.close()

            if not rows:
                return "No recent documents found."

            lines = ["Recent documents:", ""]

            for row in rows:
                if isinstance(row, dict):
                    title = row.get("title", "Untitled")
                    category = row.get("category", "Other")
                else:
                    title = row[0]
                    category = row[1]

                lines.append(f"• {title} ({category})")

            return "\n".join(lines)

        except Exception as e:
            return f"Unable to load recent documents: {str(e)}"

    def load_latest_document(self):
        response = self.summarize_latest_document()
        self.add_message("AI Assistant", response)

    def extract_document_information(self, info_type):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute(
            """
            SELECT title, category, file_path
            FROM documents
            ORDER BY upload_date DESC
            LIMIT 1
            """
            )

            row = cur.fetchone()

            cur.close()
            conn.close()

            if not row:
                return "No documents found in the repository."

            if isinstance(row, dict):
                title = row.get("title")
                category = row.get("category")
                file_path = row.get("file_path")
            else:
                title = row[0]
                category = row[1]
                file_path = row[2]

            text = extract_text_from_pdf(file_path)

            import re

            if info_type == "nid":
                m = re.search(r"\b\d{10,17}\b", text)
                value = m.group(0) if m else "Not detected"
                return f"Latest document: {title}\nNID Number: {value}\nConfidence: High"

            elif info_type == "passport":
                m = re.search(r"\b[A-Z]{1,2}\d{6,8}\b", text)
                value = m.group(0) if m else "Not detected"
                return f"Latest document: {title}\nPassport Number: {value}\nConfidence: Medium"

            elif info_type == "expiry":
                m = re.search(r"\b\d{2}[/-]\d{2}[/-]\d{4}\b", text)
                value = m.group(0) if m else "Not detected"
                return f"Latest document: {title}\nExpiry Date: {value}"

            elif info_type == "amount":
                m = re.search(r"(?:Tk|BDT|USD|EUR)?\s?\d+(?:,\d{3})*(?:\.\d{2})?", text)
                value = m.group(0) if m else "Not detected"
                return f"Latest document: {title}\nDetected Amount: {value}"

            elif info_type == "approval":
                if category and category.lower() in ["nid", "passport", "invoice", "contract"]:
                    return f"Yes. The latest document ({title}) should be submitted for approval based on its category ({category})."
                return f"Approval is optional for the latest document ({title})."

            elif info_type == "name":
                lines = [x.strip() for x in text.splitlines() if x.strip()]
                value = lines[0] if lines else "Name not detected"
                return f"Latest document: {title}\nApplicant Name: {value}\nConfidence: Medium"

            return "Information not available."

        except Exception as e:
            return f"Information extraction failed: {str(e)}"