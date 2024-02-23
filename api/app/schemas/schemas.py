import asyncio
import typing as t
from enum import Enum
from typing import Optional

import pymongo
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from pymongo import IndexModel


class GeoObjectPoint(BaseModel):
    type: str = "Point"
    coordinates: t.Tuple[float, float]


class GeoObjectPolygon(BaseModel):
    type: str = "Polygon"
    coordinates: t.List[t.List[t.Tuple[float, float]]]


class GeoObjectMultiPolygon(BaseModel):
    type: str = "MultiPolygon"
    coordinates: t.List[t.List[t.List[t.Tuple[float, float]]]]


class Geometry(BaseModel):
    type: str
    coordinates: t.Any


class Parcel(BaseModel):
    objectid: int
    area: float
    crop_type: str
    geometry: Geometry
    stats_min: float
    stats_max: float
    stats_mean: float
    stats_count: int

class ParcelDB(Document, Parcel):
    class Settings:
        name = "Parcel"
        indexes = [
            IndexModel([("objectid", pymongo.ASCENDING)], unique=True),
            IndexModel([("area", pymongo.ASCENDING)]),
            IndexModel([("crop_type", pymongo.ASCENDING)]),
            IndexModel([("geometry", pymongo.GEOSPHERE)]),
        ]
