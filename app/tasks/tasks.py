from app.tasks.celery import celery
from app.extradata.utils import ImagePlugin
import asyncio


@celery.task
def fit_image(image_id, sizes_dict, crud):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ImagePlugin.fit_image(image_id, sizes_dict, crud))
