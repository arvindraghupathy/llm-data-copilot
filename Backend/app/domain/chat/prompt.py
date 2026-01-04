def build_prompt(
    *,
    context_chunks: list[str],
    user_question: str,
) -> list[dict]:
    system_prompt = f"""
You are an assistant answering questions using ONLY the provided context.
If the answer is not in the context, say "I don't know".

Context:
{"\n\n".join(context_chunks)}
""".strip()

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]
