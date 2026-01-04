import { DatasetStatus } from "@/lib/types";

const styles: Record<DatasetStatus, string> = {
  uploaded: "bg-zinc-100 text-zinc-600",
  ingesting: "bg-amber-100 text-amber-700",
  ready: "bg-emerald-100 text-emerald-700",
  failed: "bg-rose-100 text-rose-700",
};

export function StatusBadge({ status }: { status: DatasetStatus }) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-medium ${styles[status]}`}
    >
      {status}
    </span>
  );
}
