import pymupdf as fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""

        for page in doc:
            text += page.get_text()

        doc.close()

        return text.strip()

    except Exception:
        return ""


def summarize_text(text):
    if not text:
        return "No readable text found in the PDF document."

    words = text.split()

    if len(words) <= 60:
        return text

    return " ".join(words[:60]) + "..."