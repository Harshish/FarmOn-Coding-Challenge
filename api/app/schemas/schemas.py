import asyncio
import typing as t
from enum import Enum
from typing import Optional

import pymongo
from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
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
