import Link from "next/link";

export function EmptyState() {
  return (
    <div className="rounded-xl bg-white p-12 text-center shadow-sm">
      <div className="text-lg font-medium text-zinc-900">No datasets yet</div>
      <p className="mt-2 text-zinc-500">Upload an Excel file to get started.</p>

      <Link
        href="/upload"
        className="inline-block mt-6 rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 transition"
      >
        Upload dataset
      </Link>
    </div>
  );
}
