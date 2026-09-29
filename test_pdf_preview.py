import customtkinter as ctk
from gui.pdf_preview import PDFPreviewWindow

root = ctk.CTk()
root.withdraw()

PDFPreviewWindow(
    root,
    "storage/uploads/sample.pdf",
    "Sample PDF"
)

root.mainloop()