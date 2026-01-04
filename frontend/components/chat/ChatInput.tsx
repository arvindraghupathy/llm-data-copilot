"use client";

import { useState } from "react";

export function ChatInput({
  onSend,
  disabled,
}: {
  onSend: (text: string) => void;
  disabled: boolean;
}) {
  const [text, setText] = useState("");

  function submit() {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  }

  return (
    <div className="border-t p-3 flex gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        disabled={disabled}
        placeholder="Ask a question…"
        className="flex-1 rounded-md border px-3 py-2 text-sm"
      />
      <button
        onClick={submit}
        disabled={disabled}
        className="rounded-md bg-black px-4 py-2 text-sm text-white disabled:opacity-50"
      >
        Send
      </button>
    </div>
  );
}
