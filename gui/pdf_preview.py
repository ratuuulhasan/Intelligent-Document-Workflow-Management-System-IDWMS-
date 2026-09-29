import customtkinter as ctk
import pymupdf as fitz
from PIL import Image

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class PDFPreviewWindow(ctk.CTkToplevel):

    def __init__(self, parent, pdf_path, title):
        super().__init__(parent)

        self.pdf_path = pdf_path

        self.title(f"PDF Preview - {title}")
        self.geometry("900x700")

        ctk.CTkLabel(
            self,
            text=f"PDF Preview: {title}",
            font=(None, 22, "bold")
        ).pack(pady=15)

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkButton(
            self,
            text="Close",
            width=120,
            command=self.destroy
        ).pack(pady=10)

        self.show_first_page()

    def show_first_page(self):

        try:

            doc = fitz.open(self.pdf_path)

            page = doc.load_page(0)

            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            preview = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(500, 650)
            )

            self.image_label.configure(image=preview, text="")
            self.image_label.image = preview

            doc.close()

        except Exception as e:

            self.image_label.configure(
                text=f"Preview Error:\n{e}"
            )