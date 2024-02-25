from app.db.db import get_db
from app.schemas.schemas import ParcelDB
from beanie import init_beanie
from fastapi import FastAPI
import logging
import sys

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

    parcels.logger = logging.getLogger(__name__)
    parcels.logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
    stream_handler.setFormatter(log_formatter)
    parcels.logger.addHandler(stream_handler)

app.include_router(parcels.router)

@app.get("/")
async def root():
    return {"message": "All Creatures Welcome!"}
