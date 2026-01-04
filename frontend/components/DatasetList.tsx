"use client";

import { useEffect, useState } from "react";
import { API_BASE, listDatasets } from "@/lib/api";
import { Dataset } from "@/lib/types";
import { EmptyState } from "./EmptyState";
import { DatasetRow } from "./DatasetRow";

export function DatasetList() {
  const [datasets, setDatasets] = useState<Dataset[] | null>(null);

  useEffect(() => {
    const es = new EventSource(`${API_BASE}/datasets/status/stream`);

    es.onmessage = (e) => {
      const event = JSON.parse(e.data);

      if (event.type === "dataset_status") {
        setDatasets((prev) =>
          prev
            ? prev.map((d) =>
                d.dataset_id === event.dataset_id
                  ? { ...d, status: event.status }
                  : d
              )
            : prev
        );
      }
    };

    return () => es.close();
  }, []);

  useEffect(() => {
    let canceled = false;
    listDatasets().then((data) => {
      if (!canceled) {
        setDatasets(data);
      }
    });
    return () => {
      canceled = true;
    };
  }, []);

  if (datasets === null) {
    return (
      <div className="rounded-xl border border-zinc-200 bg-white p-6 text-sm text-zinc-600 shadow-sm">
        Loading datasets…
      </div>
    );
  }

  if (datasets.length === 0) {
    return <EmptyState />;
  }

  return (
    <table className="w-full border-collapse border border-gray-400 bg-white text-sm dark:border-gray-500 dark:bg-gray-800">
      <thead className="bg-gray-50 dark:bg-gray-700">
        <tr>
          <th className="w-1/2 border border-gray-300 p-4 text-left font-semibold text-gray-900 dark:border-gray-600 dark:text-gray-200">
            Name
          </th>
          <th className="w-1/2 border border-gray-300 p-4 text-left font-semibold text-gray-900 dark:border-gray-600 dark:text-gray-200">
            Uploaded
          </th>
          <th className="w-1/2 border border-gray-300 p-4 text-left font-semibold text-gray-900 dark:border-gray-600 dark:text-gray-200">
            Status
          </th>
          <th className="w-1/2 border border-gray-300 p-4 text-left font-semibold text-gray-900 dark:border-gray-600 dark:text-gray-200">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        {datasets.map((d) => (
          <DatasetRow
            key={d.dataset_id}
            dataset={d}
            onDeleted={() =>
              setDatasets((prev) =>
                prev ? prev.filter((x) => x.dataset_id !== d.dataset_id) : prev
              )
            }
          />
        ))}
      </tbody>
    </table>
  );
}
