"""Download generated image and upload to S3 to resolve provider URL expiry."""
import boto3
import hashlib
import requests


def cache_to_s3(url: str, prompt: str, bucket: str,
                prefix: str = "img-gen") -> str:
    """
    Download generated image and upload to S3. Returns permanent S3 URL.
    Resolves DALL-E/Flux pre-signed URL expiry (~1 hour).
    Idempotent: checks S3 before downloading.
    """
    key = hashlib.sha256(prompt.strip().lower().encode()).hexdigest()[:16]
    ext = "webp" if "webp" in url else "png"
    s3_key = f"{prefix}/{key}.{ext}"
    s3 = boto3.client("s3")

    # Check if already uploaded — avoid re-downloading
    try:
        s3.head_object(Bucket=bucket, Key=s3_key)
        return f"https://{bucket}.s3.amazonaws.com/{s3_key}"
    except s3.exceptions.ClientError:
        pass

    data = requests.get(url, timeout=30).content
    s3.put_object(Bucket=bucket, Key=s3_key, Body=data,
                  ContentType=f"image/{ext}")
    return f"https://{bucket}.s3.amazonaws.com/{s3_key}"


