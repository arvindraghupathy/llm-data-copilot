"use client";

import { UploadForm } from "@/components/UploadForm";
import { uploadDocument } from "@/lib/api";

export function DatasetDocumentUploadForm({
  datasetId,
}: {
  datasetId: string;
}) {
  return (
    <>
      <div>
        <h3 className="text-3xl font-semibold tracking-tight">
          Upload supplemental documents
        </h3>
        <p className="mt-2 text-zinc-500">
          Upload supplemental documents to help the model answer questions about
          the dataset.
        </p>
      </div>
      <UploadForm
        accept=".docx"
        handleUpload={async (file) => {
          await uploadDocument(datasetId, file);
          alert("Document uploaded");
        }}
      />
    </>
  );
}
