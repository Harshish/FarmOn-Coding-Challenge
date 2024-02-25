import typing as t

from app.schemas.schemas import Parcel, ParcelDB
from fastapi import APIRouter, Query
from shapely.geometry import mapping, shape
from bson.son import SON
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from beanie.odm.operators.find.geospatial import Near

logger = None
MAX_DISTANCE = 100000

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
    if not isinstance(parcels, list):
        parcels = [parcels]
    if len(parcels) > 50:
        return [
            "Too many parcels to add at once. Please add 50 or fewer parcels at a time."
        ]
    success = []
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
) -> ParcelDB | str:
    geometry = [Point((longitude,latitude))]

    df = pd.DataFrame({'longitude': [longitude], 'latitude': [latitude]})
    geometry = gpd.points_from_xy(df.longitude, df.latitude, crs=crs)
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs=crs)
    gdf = gdf.to_crs("EPSG:4326")

    x, y = gdf.iloc[0]["geometry"].x, gdf.iloc[0]["geometry"].y
    logger.debug(f"Queried coords: {x},{y}")
    try:
        query = Near(ParcelDB.centroid, x, y, min_distance=0, max_distance=MAX_DISTANCE)
        logger.debug(query)
        val = await ParcelDB.find_one(query)
        if not val:
            return f"No feilds found within radius {MAX_DISTANCE} m"
        return val
    except Exception as e:
        return repr(e)