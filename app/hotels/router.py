from fastapi.responses import JSONResponse
from fastapi import FastAPI, Query, APIRouter, Body, status, Depends, UploadFile, File
from .dependecies import HotelsSearchArgs
from .models import Hotel, ServiceTypes
from .service import HotelsCRUD, ServiceTypeCRUD
from typing import List
from app.s3 import upload

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
    '/{id}',
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
    print(content, "content")
    if not content:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'error': 'Hotel not found'})
    return JSONResponse(status_code=status.HTTP_200_OK, content={'status': 'Ok',
                                                                 'message': 'Hotel and related data successfully '
                                                                            'removed'})


@router.get(
    '/get_hotels',
    response_model=list[Hotel],
    status_code=status.HTTP_200_OK,
    description='Get all hotels'
)
async def get_hotels(search_args: HotelsSearchArgs = Depends()
                     ):
    response = await HotelsCRUD.get_hotels(search_args)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)


@router.post(
    '/service_types/create_new',
    response_model=ServiceTypes,
    status_code=status.HTTP_201_CREATED,
    description='Create new service type'
)
async def create_service_type(file: UploadFile = File(...), service: ServiceTypes = Depends()):
    # TO-DO check file type, size, mime-type and meta-data
    url = await upload(file.filename, file, 'service_types_logo')
    service.logo_url = url
    content = await ServiceTypeCRUD.create(service)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)


@router.get(
    'service_types/get_service_type/{service_type_name}',
    response_model=ServiceTypes,
    status_code=status.HTTP_200_OK,
    description='Get service type by name'
)
async def get_service_type(service_type_name):
    content = await ServiceTypeCRUD.get(service_type_name)
    return JSONResponse(status_code=status.HTTP_200_OK, content=content)
