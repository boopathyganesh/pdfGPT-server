def split_text_to_chunks(text: str, max_tokens: int = 500) -> list[str]:
    text = text.replace('\r', '').replace('\t', ' ').replace('\n\n', '\n')
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(para.split()) > max_tokens:
            words = para.split()
            for i in range(0, len(words), max_tokens):
                chunks.append(" ".join(words[i:i + max_tokens]))
        elif len((current_chunk + para).split()) > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"
        else:
            current_chunk += para + "\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    #print(f"[split_text_to_chunks] Input length: {len(text)} characters")
    #print(f"[split_text_to_chunks] Total chunks created: {len(chunks)}")

    return chunks
