from typing import BinaryIO

from miniopy_async import Minio

from src.config.settings import settings

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)


async def upload_file(file: BinaryIO, object_name: str) -> str:
    """Upload file to minio storage.

    Args:
        file: File-like object to upload.
        object_name: Name of the object in minio storage.

    Returns:
        str: URL of the uploaded file.
    """
    bucket_name = settings.MINIO_PUBLIC_BUCKET

    # Ensure bucket exists
    bucket_exists = await minio_client.bucket_exists(bucket_name)
    if not bucket_exists:
        await minio_client.make_bucket(bucket_name)

    # Upload file
    await minio_client.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=file,
        length=-1,  # Let minio calculate the length
        part_size=10 * 1024 * 1024,  # 10MB chunks
    )
    # TODO: Change return file url like https://minio.dip-analytics.ru/public/1234567890.pdf

    return f"{settings.MINIO_ENDPOINT}/{bucket_name}/{object_name}"


async def delete_file(object_name: str) -> None:
    """Delete file from minio storage.

    Args:
        object_name: Name of the object in minio storage.
    """
    await minio_client.remove_object(settings.MINIO_PUBLIC_BUCKET, object_name)
