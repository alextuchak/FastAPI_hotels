from miniopy_async import Minio
from app.settings import settings


class S3:
    client = Minio(endpoint=settings.MINIO_ENDPOINT, access_key=settings.ACCESS_KEY, secret_key=settings.SECRET_KEY,
                   secure=False)

    @classmethod
    async def upload(cls, file_name, file):
        await cls.client.put_object(settings.MINIO_BUCKET, file_name, file, part_size=10 * 1024 * 1024,
                                    length=-1)
        url = await cls.download(file_name)
        return url

    @classmethod
    async def download(cls, file_name):
        url = await cls.client.presigned_get_object(settings.MINIO_BUCKET, file_name)
        return url
