import { Dataset } from "./types";

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE!;

export async function listDatasets(): Promise<Dataset[]> {
  const res = await fetch(`${API_BASE}/datasets/list`);
  if (!res.ok) throw new Error("Failed to load datasets");
  return res.json();
}

export async function uploadDataset(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/datasets/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}

export async function deleteDataset(datasetId: string) {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error("Failed to delete dataset");
  }
}

export async function getDataset(datasetId: string) {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Dataset not found");
  }

  return res.json();
}

export async function sendChatMessage(
  datasetId: string,
  messages: { role: "user" | "assistant"; content: string }[]
) {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  if (!res.ok) {
    throw new Error("Chat failed");
  }

  return res.json() as Promise<{ answer: string }>;
}

export type Citation = {
  filename: string;
  source: "excel" | "docx";
  sheet?: string;
  row_index?: number;
};

export type StreamEvent =
  | { type: "token"; content: string }
  | { type: "citations"; citations: Citation[] }
  | { type: "result"; rows: Record<string, unknown>[] };

export async function streamChat(
  datasetId: string,
  messages: { role: "user" | "assistant"; content: string }[],
  onEvent: (event: StreamEvent) => void,
  onDone: () => void
) {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    },
    body: JSON.stringify({ messages }),
  });

  if (!res.body) {
    throw new Error("No response body");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();

  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() || "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;

      const payload = line.slice(6).trim();

      if (payload === "[DONE]") {
        onDone();
        return;
      }

      try {
        const event = JSON.parse(payload);
        onEvent(event);
      } catch {
        // ignore malformed chunks
      }
    }
  }
}

export async function listDatasetRows(
  datasetId: string,
  page: number,
  pageSize: number
): Promise<{ rows: Record<string, unknown>[]; total: number }> {
  console.log(
    `${API_BASE}/datasets/${datasetId}/rows?page=${page}&page_size=${pageSize}`
  );
  const res = await fetch(
    `${API_BASE}/datasets/${datasetId}/rows?page=${page}&page_size=${pageSize}`,
    { cache: "no-store" }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch dataset rows");
  }

  return res.json();
}

export async function uploadDocument(datasetId: string, file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(
    `${API_BASE}/datasets/${datasetId}/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Upload failed");
  }
}

export async function listDocuments(datasetId: string) {
  const res = await fetch(`${API_BASE}/datasets/${datasetId}/documents`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch documents");
  }

  return res.json();
}
