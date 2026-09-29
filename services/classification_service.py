def classify_document(text):
    if not text:
        return "Other"

    t = text.lower()

    if "national id" in t or "nid" in t:
        return "NID"

    if "passport" in t:
        return "Passport"

    if "invoice" in t or "tax invoice" in t:
        return "Invoice"

    if "certificate" in t:
        return "Certificate"

    if "agreement" in t or "contract" in t:
        return "Contract"

    return "Other"