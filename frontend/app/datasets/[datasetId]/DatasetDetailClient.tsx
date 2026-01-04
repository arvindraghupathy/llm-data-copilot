"use client";

import { StatusBadge } from "@/components/StatusBadge";
import { API_BASE } from "@/lib/api";
import { Dataset, DatasetStatus } from "@/lib/types";
import Link from "next/link";
import { useEffect, useState } from "react";

export function DatasetDetailClient({ dataset }: { dataset: Dataset }) {
  const [status, setStatus] = useState<DatasetStatus>(dataset.status);
  useEffect(() => {
    if (status === "ready" || status === "failed") return;

    const es = new EventSource(
      `${API_BASE}/datasets/${dataset.dataset_id}/status/stream`
    );

    es.onmessage = (e) => {
      const event = JSON.parse(e.data);

      if (event.type === "dataset_status") {
        setStatus(event.status);

        if (event.status === "ready" || event.status === "failed") {
          es.close();
        }
      }
    };

    return () => es.close();
  }, [dataset.dataset_id, status]);
  return (
    <>
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight">
            {dataset.filename}
          </h1>
          <p className="mt-2 text-zinc-500">
            Uploaded {new Date(dataset.created_at).toLocaleString()}
          </p>
        </div>

        <StatusBadge status={status} />
      </div>

      {/* Info cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <InfoCard label="Status" value={dataset.status} />
        <InfoCard label="Dataset ID" value={dataset.dataset_id} mono />
      </div>

      {/* CTA */}
      <div className="rounded-xl bg-white p-6 shadow-sm border border-zinc-100">
        <h2 className="text-lg font-medium">
          Ask questions about this dataset
        </h2>

        <p className="mt-1 text-sm text-zinc-500">
          Use natural language to explore and query your data.
        </p>

        <div className="mt-4">
          <button
            disabled={dataset.status !== "ready"}
            className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
          >
            <Link href={`/datasets/${dataset.dataset_id}/chat`}>Open chat</Link>
          </button>

          {dataset.status !== "ready" && (
            <p className="mt-2 text-xs text-zinc-500">
              Chat will be available once ingestion completes.
            </p>
          )}
        </div>
      </div>
      <div className="rounded-xl bg-white p-6 shadow-sm border border-zinc-100">
        <h2 className="text-lg font-medium">View dataset contents</h2>

        <p className="mt-1 text-sm text-zinc-500">
          View the contents of the dataset.
        </p>

        <div className="mt-4">
          <button className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white disabled:opacity-40">
            <Link href={`/datasets/${dataset.dataset_id}/table`}>
              Open table
            </Link>
          </button>
        </div>
      </div>
    </>
  );
}
function InfoCard({
  label,
  value,
  mono = false,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div className="rounded-xl bg-white p-4 shadow-sm border border-zinc-100">
      <div className="text-xs uppercase tracking-wide text-zinc-500">
        {label}
      </div>
      <div className={`mt-1 text-sm ${mono ? "font-mono" : ""}`}>{value}</div>
    </div>
  );
}
