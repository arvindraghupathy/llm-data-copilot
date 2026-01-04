import { Dataset } from "@/lib/types";
import { StatusBadge } from "./StatusBadge";
import { deleteDataset } from "@/lib/api";
import Link from "next/link";

export function DatasetRow({
  dataset,
  onDeleted,
}: {
  dataset: Dataset;
  onDeleted: () => void;
}) {
  async function handleDelete() {
    const ok = confirm(`Delete "${dataset.filename}"?\nThis cannot be undone.`);
    if (!ok) return;

    await deleteDataset(dataset.dataset_id);
    onDeleted();
  }
  return (
    <tr className="">
      <td className="border border-gray-300 p-4 text-gray-500 dark:border-gray-700 dark:text-gray-400">
        <Link href={`/datasets/${dataset.dataset_id}`}>{dataset.filename}</Link>
      </td>
      <td className="border border-gray-300 p-4 text-gray-500 dark:border-gray-700 dark:text-gray-400">
        {new Date(dataset.created_at).toLocaleDateString()}
      </td>
      <td className="border border-gray-300 p-4 text-gray-500 dark:border-gray-700 dark:text-gray-400">
        <StatusBadge status={dataset.status} />
      </td>
      <td className="border border-gray-300 p-4 text-gray-500 dark:border-gray-700 dark:text-gray-400">
        <button onClick={handleDelete} className="text-red-500">
          Delete
        </button>
      </td>
    </tr>
  );
}
