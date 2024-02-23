import typing as t

import pymongo
from beanie import Document
from pydantic import BaseModel
from pymongo import IndexModel


class Geometry(BaseModel):
    type: str
    coordinates: t.Any


class Parcel(BaseModel):
    objectid: int
    area: float
    crop_type: str
    geometry: Geometry

class ParcelDB(Document, Parcel):
    class Settings:
        name = "Parcel"
        indexes = [
            IndexModel([("objectid", pymongo.ASCENDING)], unique=True),
            IndexModel([("area", pymongo.ASCENDING)]),
            IndexModel([("crop_type", pymongo.ASCENDING)]),
            IndexModel([("geometry", pymongo.GEOSPHERE)]),
        ]
