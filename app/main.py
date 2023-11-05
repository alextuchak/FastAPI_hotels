from fastapi import FastAPI, APIRouter
from .database import db
from app.hotels.router import router as hotels_routers

app = FastAPI()

app.include_router(hotels_routers)


@app.get('/db')
async def asda():
    collection = db['hotels']
    return True
