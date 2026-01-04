"use client";

import { useParams } from "next/navigation";
import { DatasetTable } from "@/components/dataset/DatasetTable";
import Link from "next/link";

export default function DatasetTablePage() {
  const { datasetId } = useParams<{ datasetId: string }>();

  return (
    <div className="max-w-7xl mx-auto px-6 py-8 space-y-6">
      <Link
        href={`/datasets/${datasetId}`}
        className="text-sm text-zinc-500 mb-4"
      >
        ← Back to dataset
      </Link>
      <h1 className="text-2xl font-semibold">Dataset contents</h1>
      <DatasetTable datasetId={datasetId} />
    </div>
  );
}
