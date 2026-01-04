import Link from "next/link";

export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">
        <div className="font-semibold text-lg">RAG Playground</div>
        <Link
          href="/upload"
          className="px-4 py-2 text-sm rounded bg-black text-white"
        >
          Upload Dataset
        </Link>
      </div>
    </header>
  );
}
