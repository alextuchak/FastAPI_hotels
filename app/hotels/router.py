from fastapi.responses import JSONResponse
from fastapi_events.dispatcher import dispatch
from fastapi import APIRouter, Body, status, Depends, UploadFile, File
from .dependecies import HotelsSearchArgs, ServiceTypesArgs
from .models import Hotel, ServiceTypes
from .service import HotelsCRUD, ServiceTypeCRUD
from app.extradata.utils import ImagePlugin
from app.s3 import S3

router = APIRouter(
    prefix='/hotels',
)


@router.post(
    '/test_db',
    response_model=Hotel,
    status_code=status.HTTP_201_CREATED,
    description="New hotel creation",
)
async def create_hotel(hotel: Hotel = Body(...)):
    content = await HotelsCRUD.create(hotel)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.get(
    '/find_one/{id}',
    response_model=Hotel,
    status_code=status.HTTP_200_OK,
    description="Get hotel by id"
)
async def get_hotel(id):
    content = await HotelsCRUD.get_one(id)
    if not content:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Hotel not found'})
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)


@router.delete(
    '/{id}',
    status_code=status.HTTP_200_OK,
    description="Delete hotel by id"
)
async def delete_hotel(id):
    content = await HotelsCRUD.delete_one(id)
    if not content:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Hotel not found'})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'status': 'Ok',
                                                                 'message': 'Hotel and related data successfully '
                                                                            'removed'})


@router.get(
    '/find_hotels',
    response_model=list[Hotel],
    status_code=status.HTTP_200_OK,
    description='Find hotels'
)
async def get_all_hotels(search_args: HotelsSearchArgs = Depends()
                         ):
    dispatch("cat1", payload={1: "1"})
    response = await HotelsCRUD.get_hotels(search_args)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post(
    '/service_types/create_new',
    response_model=ServiceTypes,
    status_code=status.HTTP_201_CREATED,
    description='Create new service type'
)
async def create_service_type(service: ServiceTypesArgs = Depends(), file: UploadFile = File(...), ):
    # To-do create class for with all following logic which takes data and crud class
    check, buffer, sizes_dict, hash_name = await ImagePlugin.check_image(file)
    if not check:
        pass
    url = await S3.upload(hash_name, buffer)
    updated_service = ServiceTypes(name=service.name,
                                   media={'origin': url})
    content = await ServiceTypeCRUD.create(updated_service)
    dispatch(event_name="image_upload", payload={"image_id": content['_id'], "sizes_dict": sizes_dict,
                                                 "crud": ServiceTypeCRUD.__name__})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.get(
    'service_types/get_service_type/{service_type_id}',
    response_model=ServiceTypes,
    status_code=status.HTTP_200_OK,
    description='Get service type by id'
)
async def get_service_type(service_type_id: str):
    content = await ServiceTypeCRUD.get_one(service_type_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
