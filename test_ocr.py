from services.ocr_service import extract_text

text = extract_text("storage/uploads/nid_card.png")

print(text)