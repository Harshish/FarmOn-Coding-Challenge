from app.db.db import get_db
from app.schemas.schemas import ParcelDB
from beanie import init_beanie
from fastapi import FastAPI

from .routers import parcels

app = FastAPI(
    title="FarmOn Insights API",
    description="This is the API for the FarmOn Insights application.",
    version="0.0.1",
)


@app.on_event("startup")
async def on_startup():
    db = await get_db()
    await init_beanie(
        database=db,
        document_models=[ParcelDB],
    )


app.include_router(parcels.router)

@app.get("/")
async def root():
    return {"message": "All Creatures Welcome!"}
