"use client";

import { useEffect, useState } from "react";
import { listDatasetRows } from "@/lib/api";
import { DatasetTablePagination } from "@/components/dataset/DatasetTablePagination";

const PAGE_SIZE = 25;

export function DatasetTable({ datasetId }: { datasetId: string }) {
  const [rows, setRows] = useState<Record<string, unknown>[]>([]);
  const [columns, setColumns] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    listDatasetRows(datasetId, page, PAGE_SIZE)
      .then((data) => {
        if (!active) return;
        setRows(data.rows);
        setTotal(data.total);

        if (data.rows.length > 0) {
          setColumns(Object.keys(data.rows[0]));
        }
      })
      .finally(() => active && setLoading(false));

    return () => {
      active = false;
    };
  }, [datasetId, page]);

  const handlePageChange = (newPage: number) => {
    setLoading(true);
    setPage(newPage);
  };

  if (loading) {
    return (
      <div className="rounded-lg border bg-white p-6 text-sm">
        Loading rows…
      </div>
    );
  }

  if (rows.length === 0) {
    return (
      <div className="rounded-lg border bg-white p-6 text-sm">
        No rows found.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="overflow-x-auto rounded-lg border bg-white">
        <table className="min-w-full text-sm">
          <thead className="bg-zinc-50">
            <tr>
              {columns.map((col) => (
                <th
                  key={col}
                  className="border-b px-4 py-2 text-left font-medium text-zinc-700"
                >
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={idx} className="odd:bg-white even:bg-zinc-50">
                {columns.map((col) => (
                  <td key={col} className="border-b px-4 py-2 text-zinc-800">
                    {String(row[col] ?? "")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <DatasetTablePagination
        page={page}
        pageSize={PAGE_SIZE}
        total={total}
        onPageChange={handlePageChange}
      />
    </div>
  );
}
