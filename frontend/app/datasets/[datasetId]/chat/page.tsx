import Link from "next/link";
import { ChatPanel } from "@/components/chat/ChatPanel";

export default async function ChatPage({
  params,
}: {
  params: Promise<{ datasetId: string }>;
}) {
  const { datasetId } = await params;
  return (
    <main className="flex flex-col h-screen max-w-4xl mx-auto px-6 py-6">
      <Link
        href={`/datasets/${datasetId}`}
        className="text-sm text-zinc-500 mb-4"
      >
        ← Back to dataset
      </Link>

      <ChatPanel datasetId={datasetId} />
    </main>
  );
}
