"use client";

import { useEffect, useState } from "react";
import { listDocuments } from "@/lib/api";

type DocumentItem = {
  id: string;
  filename: string;
  content_type: string;
  created_at: string;
};

export function DocumentList({ datasetId }: { datasetId: string }) {
  const [docs, setDocs] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    listDocuments(datasetId)
      .then((data) => active && setDocs(data))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, [datasetId]);

  if (loading) {
    return (
      <div className="rounded-lg border bg-white p-4 text-sm">
        Loading documents…
      </div>
    );
  }

  if (docs.length === 0) {
    return (
      <div className="rounded-lg border bg-white p-4 text-sm text-zinc-600">
        No supplemental documents uploaded.
      </div>
    );
  }

  return (
    <div className="rounded-lg border bg-white p-4 space-y-3">
      <h3 className="font-medium">Supplemental documents</h3>

      <ul className="divide-y text-sm">
        {docs.map((doc) => (
          <li key={doc.id} className="py-2 flex justify-between">
            <span>{doc.filename}</span>
            <span className="text-zinc-500">
              {new Date(doc.created_at).toLocaleString()}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
