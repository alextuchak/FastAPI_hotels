from miniopy_async import Minio
from app.settings import settings


client = Minio(endpoint=settings.MINIO_ENDPOINT, access_key=settings.ACCESS_KEY, secret_key=settings.SECRET_KEY,
               secure=False)


async def upload(file_name, file, folder_name):
    await client.put_object(settings.MINIO_BUCKET, folder_name + '/' + file_name, file, part_size=10 * 1024 * 1024,
                            length=-1)
    url = await client.presigned_get_object(settings.MINIO_BUCKET, folder_name + '/' + file_name)
    return url

