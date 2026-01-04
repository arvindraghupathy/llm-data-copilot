"use client";

type ResultTableProps = {
  rows: Record<string, unknown>[];
};

export function ResultTable({ rows }: ResultTableProps) {
  if (!rows || rows.length === 0) {
    return null;
  }

  // Extract column names dynamically
  const columns = Object.keys(rows[0]);

  return (
    <div className="mt-4 overflow-x-auto rounded-lg border bg-white">
      <table className="min-w-full border-collapse text-sm">
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
          {rows.map((row, i) => (
            <tr key={i} className="odd:bg-white even:bg-zinc-50">
              {columns.map((col) => (
                <td key={col} className="px-4 py-2 text-zinc-800">
                  {String(row[col] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
