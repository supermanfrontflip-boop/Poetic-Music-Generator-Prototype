# storage.py
import os
import uuid
from urllib.parse import urljoin
from dotenv import load_dotenv
load_dotenv()

STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "/tmp/pmg_storage")

if STORAGE_BACKEND == "s3":
    import boto3
    S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
    s3 = boto3.client("s3", endpoint_url=S3_ENDPOINT,
                      aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

def ensure_local_dir():
    os.makedirs(LOCAL_STORAGE_PATH, exist_ok=True)

def save_bytes(filename: str, data: bytes) -> str:
    """Save raw bytes and return accessible URL or path"""
    if STORAGE_BACKEND == "s3":
        key = f"{uuid.uuid4().hex}/{filename}"
        s3.put_object(Bucket=S3_BUCKET, Key=key, Body=data)
        return f"{S3_ENDPOINT.rstrip('/')}/{S3_BUCKET}/{key}"
    else:
        ensure_local_dir()
        path = os.path.join(LOCAL_STORAGE_PATH, filename)
        with open(path, "wb") as f:
            f.write(data)
        return f"file://{path}"

def save_file_from_path(src_path: str, filename: str = None) -> str:
    """Copy a local file into storage and return its URL/path"""
    if not filename:
        filename = os.path.basename(src_path)
    with open(src_path, "rb") as f:
        data = f.read()
    return save_bytes(filename, data)