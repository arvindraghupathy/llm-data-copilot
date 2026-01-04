REWRITE_PROMPT = """
You are a query rewriter.

Given the conversation so far and the user's latest question,
rewrite the latest question into a standalone, fully-specified question.

Rules:
- Do NOT answer the question
- Do NOT add new information
- Preserve the user's intent
- Make implicit references explicit
- If the question is already standalone, return it unchanged

Conversation:
{conversation}

Latest question:
{question}

Standalone question:
"""
