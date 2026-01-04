import Link from "next/link";
import { getDataset } from "@/lib/api";
import { DatasetDocumentUploadForm } from "@/components/dataset/DatasetDocumentUploadForm";
import { DocumentList } from "@/components/dataset/DocumentList";
import { DatasetDetailClient } from "./DatasetDetailClient";

interface PageProps {
  params: Promise<{
    datasetId: string;
  }>;
}

export default async function DatasetDetailPage({ params }: PageProps) {
  const { datasetId } = await params;
  const dataset = await getDataset(datasetId);

  return (
    <main className="max-w-4xl mx-auto px-6 py-12 space-y-8">
      {/* Back */}
      <Link href="/" className="text-sm text-zinc-500 hover:text-zinc-700">
        ← Back to datasets
      </Link>

      <DatasetDetailClient dataset={dataset} />

      <DatasetDocumentUploadForm datasetId={datasetId} />
      <DocumentList datasetId={datasetId} />
    </main>
  );
}
