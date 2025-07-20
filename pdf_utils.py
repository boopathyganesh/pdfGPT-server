import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes, chunk_size=500) -> list[str]:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    # Simple chunking
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    return chunks
