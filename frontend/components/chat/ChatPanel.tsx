"use client";

import { useState } from "react";
import { Citation, streamChat } from "@/lib/api";
import { MessageList } from "./MessageList";
import { ChatInput } from "./ChatInput";
import { ChatMessage } from "./types";
import { ResultTable } from "../ResultTable";

export function ChatPanel({ datasetId }: { datasetId: string }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [citations, setCitations] = useState<Citation[]>([]);
  const [analysisRows, setAnalysisRows] = useState<
    Record<string, unknown>[] | null
  >(null);

  async function handleSend(text: string) {
    const userMessage: ChatMessage = {
      role: "user",
      content: text,
    };

    const assistantMessage: ChatMessage = {
      role: "assistant",
      content: "",
    };

    setMessages((prev) => [...prev, userMessage, assistantMessage]);
    setLoading(true);
    setCitations([]);
    await streamChat(
      datasetId,
      [...messages, userMessage],
      (event) => {
        if (event.type === "result") {
          setAnalysisRows(event.rows);
        }
        if (event.type === "token") {
          setMessages((prev) => {
            const copy = [...prev];
            copy[copy.length - 1] = {
              ...copy[copy.length - 1],
              content: copy[copy.length - 1].content + event.content,
            };
            return copy;
          });
        }

        if (event.type === "citations") {
          setCitations(event.citations);
        }
      },
      () => {
        setLoading(false);
      }
    );
  }

  return (
    <div className="flex flex-col flex-1 border rounded-xl bg-white shadow-sm">
      {analysisRows && <ResultTable rows={analysisRows} />}
      <MessageList messages={messages} loading={loading} />
      {citations.length > 0 && (
        <div className="mx-4 mb-2 rounded-lg border bg-zinc-50 p-3 text-sm">
          <div className="font-medium mb-2">Sources</div>
          <ul className="space-y-1">
            {citations.map((c, i) => (
              <li key={i} className="text-zinc-700">
                {c.source === "excel" && (
                  <>
                    Excel · {c.sheet} · Row {c.row_index}
                  </>
                )}
                {c.source === "docx" && <>DOCX · {c.filename}</>}
              </li>
            ))}
          </ul>
        </div>
      )}

      <ChatInput onSend={handleSend} disabled={loading} />
    </div>
  );
}
