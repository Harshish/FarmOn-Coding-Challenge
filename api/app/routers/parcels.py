import typing as t

import shapely
from app.schemas.schemas import Parcel, ParcelDB
from beanie.operators import GeoWithin, Near
from fastapi import APIRouter, Query
from pymongo import GEOSPHERE
from shapely.geometry import mapping, shape
from shapely.ops import transform

router = APIRouter(
    prefix="/parcels",
    tags=["Parcels"],
)


def validate_and_correct_geometry(geometry):
    shapely_geom = shape(dict(geometry))  # Convert to Shapely geometry
    if not shapely_geom.is_valid:
        corrected_geom = shapely_geom.buffer(0)
        return mapping(corrected_geom)  # Convert back to GeoJSON-like dict
    else:
        return geometry


@router.post("/add_parcels")
async def add_parcels(parcels: t.Union[Parcel, t.List[Parcel]]) -> t.List[str]:
    if len(parcels) > 50:
        return [
            "Too many parcels to add at once. Please add 50 or fewer parcels at a time."
        ]
    success = []
    if not isinstance(parcels, list):
        parcels = [parcels]
    for parcel in parcels:
        parcel.geometry = validate_and_correct_geometry(parcel.geometry)
        existing_doc = await ParcelDB.find_one(ParcelDB.objectid == parcel.objectid)
        if not existing_doc:
            try:
                await ParcelDB(
                    **parcel.model_dump()
                ).insert()  # Ensure to convert Pydantic model to dict
                success.append("Parcel added")
            except Exception as e:
                success.append(f"Error: {e}")
        else:
            success.append("Parcel already exists")
    return success


@router.get("/find_parcel_by_location")
async def find_parcel_by_location(
    latitude: float = Query(...),
    longitude: float = Query(...),
    crs: str = Query("EPSG:4326"),
) -> Parcel:
    pass