from fastapi_events.handlers.local import local_handler as hotels_handler
from fastapi_events.typing import Event
from app.tasks.tasks import fit_image


@hotels_handler.register(event_name="image*")
def new_image_upload(event: Event):
    payload = event[1]
    fit_image.delay(payload['image_id'], payload['sizes_dict'], payload['crud'])
