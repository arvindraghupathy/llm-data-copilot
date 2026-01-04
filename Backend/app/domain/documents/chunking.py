def chunk_text(
    text: str,
    max_chars: int = 800,
):
    chunks = []
    current = ""

    for line in text.splitlines():
        if len(current) + len(line) > max_chars:
            chunks.append(current.strip())
            current = line
        else:
            current += "\n" + line

    if current.strip():
        chunks.append(current.strip())

    return chunks
