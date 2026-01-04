import { ChatMessage } from "./types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

  return (
    <div
      className={`max-w-[75%] rounded-lg px-4 py-2 text-sm ${
        isUser ? "ml-auto bg-black text-white" : "bg-zinc-100 text-zinc-900"
      }`}
    >
      {message.content}
    </div>
  );
}
