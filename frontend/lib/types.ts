export enum DatasetStatus {
  UPLOADED = "uploaded",
  INGESTING = "ingesting",
  READY = "ready",
  FAILED = "failed",
}

export interface Dataset {
  dataset_id: string;
  filename: string;
  status: DatasetStatus;
  created_at: string;
}
