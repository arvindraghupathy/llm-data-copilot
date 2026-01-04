import Link from "next/link";
import { DatasetList } from "@/components/DatasetList";
export default function Home() {
  return (
    <main className="max-w-4xl mx-auto px-6 py-12 space-y-8">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">Datasets</h1>
          <p className="text-zinc-500 mt-1">
            Upload Excel files and query them conversationally.
          </p>
        </div>
        <Link
          href="/upload"
          className="inline-flex items-center rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 transition"
        >
          Upload
        </Link>
      </div>
      <DatasetList />
    </main>
  );
}
