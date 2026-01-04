"use client";

import { useState } from "react";

export function UploadForm({
  accept = ".xlsx,.xls",
  handleUpload,
}: {
  handleUpload: (file: File) => Promise<void> | void;
  accept?: string;
}) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleUploadClick() {
    if (!file) return;
    setLoading(true);
    try {
      await handleUpload(file);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-xl bg-white p-6 shadow-sm space-y-4">
      <input
        type="file"
        accept={accept}
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="block w-full text-sm text-zinc-600
          file:mr-4 file:rounded-lg file:border-0
          file:bg-zinc-100 file:px-4 file:py-2
          file:text-sm file:font-medium
          hover:file:bg-zinc-200"
      />

      <button
        onClick={handleUploadClick}
        disabled={!file || loading}
        className="inline-flex items-center rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 disabled:opacity-50 transition"
      >
        {loading ? "Uploading…" : "Upload"}
      </button>
    </div>
  );
}
