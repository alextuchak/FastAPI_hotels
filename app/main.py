from fastapi import FastAPI
from fastapi_events.dispatcher import dispatch
from app.hotels.router import router as hotels_routers
from app.hotels.handlers import hotels_handler
from fastapi_events.middleware import EventHandlerASGIMiddleware
from fastapi import UploadFile, File
from app.extradata.utils import ImagePlugin
from app.s3 import S3
from app.tasks.tasks import fit_image

app = FastAPI()

app.add_middleware(EventHandlerASGIMiddleware,
                   handlers=[hotels_handler])
app.include_router(hotels_routers)


@app.post('/db')
async def asda(file: UploadFile = File(...)):
    # endpoint for test - will be deleted
    check, buffer, sizes_dict, hash_name = await ImagePlugin.check_image(file)
    if check:
        dispatch(event_name="image_upload", payload={"buffer": buffer, "sizes_dict": sizes_dict,
                                                     "hash_name": hash_name, "crud": "crud"})
    url = await S3.upload(hash_name,
                          buffer)
    fit_image.delay()
    return True
