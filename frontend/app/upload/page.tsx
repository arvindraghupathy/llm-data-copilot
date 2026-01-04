"use client";
import Link from "next/link";
import { UploadForm } from "@/components/UploadForm";
import { uploadDataset } from "@/lib/api";

async function handleUpload(file: File) {
  await uploadDataset(file);
  window.location.href = "/";
}

export default function UploadPage() {
  return (
    <main className="max-w-2xl mx-auto px-6 py-12 space-y-8">
      <Link href="/" className="text-sm text-zinc-500 hover:text-zinc-700">
        ← Back
      </Link>

      <div>
        <h1 className="text-3xl font-semibold tracking-tight">
          Upload dataset
        </h1>
        <p className="mt-2 text-zinc-500">
          Upload an Excel file to ingest and query conversationally.
        </p>
      </div>

      <UploadForm handleUpload={handleUpload} />
    </main>
  );
}
