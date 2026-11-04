"""Optional AWS S3 landing-zone adapter. Uses the standard boto3 credential chain."""
from __future__ import annotations

import os
from pathlib import Path

import boto3


def upload_landing_file(file_path: str, object_key: str | None = None) -> str:
    bucket = os.environ["AWS_S3_BUCKET"]
    path = Path(file_path)
    key = object_key or f"raw/api_events/{path.name}"
    client = boto3.client("s3", region_name=os.getenv("AWS_REGION"))
    client.upload_file(str(path), bucket, key)
    return f"s3://{bucket}/{key}"
