from io import BytesIO
import hashlib
from aiocsv.readers import AsyncReader
import os
import aiofile
from app.settings import settings
from app.hotels.service import HotelsCRUD, ServiceTypeCRUD
from PIL import Image
from app.s3 import S3
import aiohttp


class ImagePlugin:

    CRUDS = {HotelsCRUD.__name__: HotelsCRUD,
             ServiceTypeCRUD.__name__: ServiceTypeCRUD
    }

    @classmethod
    async def check_image(cls, image):
        await image.seek(0)
        content = await image.read()
        with Image.open(BytesIO(content)) as img:
            if not await cls._check_mimes_and_exts(img.format.lower()):
                return ValueError("wrong file type")
            final_img_sizes = {key: value for key, value in settings.IMAGES_SETTINGS['images'].items() if
                               value['width'] * value['height'] < img.size[0] * img.size[1]}
            return True, BytesIO(content), final_img_sizes, hashlib.md5(content).hexdigest()

    @classmethod
    async def _check_mimes_and_exts(cls, file_type):
        async with aiofile.async_open(os.path.join(path, 'mimes_and_exts.csv'), encoding='utf-8-sig') as file:
            async for row in AsyncReader(file):
                if file_type == row[2]:
                    return True
            return False

    @classmethod
    async def fit_image(cls, image_id, sizes_dict, crud):
        new_media = dict()
        data = await cls.CRUDS[crud].get_one(image_id)
        new_media['media'] = data['media']
        url = new_media['media']['origin']
        for size_name, sizes in sizes_dict.items():
            buffer = BytesIO()
            async with aiohttp.ClientSession() as session:
                content = await session.get(url)
                img_for_read = BytesIO(await content.read())
                with Image.open(img_for_read) as img:
                    img.resize((sizes['height'], sizes['width']))
                    img.save(buffer, 'png')
                    buffer.seek(0)
                    resized_img_url = await S3.upload(hashlib.md5(buffer.read()).hexdigest(), buffer)
                    buffer.close()
                    new_media['media'][size_name] = resized_img_url
        await cls.CRUDS[crud].update_one(image_id, new_media)


path = os.path.abspath('app/configs')

