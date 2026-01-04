import { ChatMessage } from "./types";
import { MessageBubble } from "./MessageBubble";

export function MessageList({
  messages,
  loading,
}: {
  messages: ChatMessage[];
  loading: boolean;
}) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((m, i) => (
        <MessageBubble key={i} message={m} />
      ))}

      {loading && (
        <div className="text-sm text-zinc-400">Assistant is typing…</div>
      )}
    </div>
  );
}
