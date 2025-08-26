# Create your models here.
# spots/models.py
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude


class SpotType(str, Enum):
    CHARGING_STATION = "charging_station"
    ORGANIC_MARKET = "organic_market"
    BIO_SHOP = "bio_shop"
    LOCAL_PRODUCER = "local_producer"
    ECO_ACCOMMODATION = "eco_accommodation"


class Spot(BaseModel):
    name: str
    type: SpotType
    latitude: Latitude
    longitude: Longitude
    address: Optional[str] = None
    description: Optional[str] = None
    opening_hours: Optional[str] = Field(None, alias="openingHours")
    website: Optional[HttpUrl] = None
    phone: Optional[str] = None
    price_range: Optional[str] = Field(None, alias="priceRange")
    power: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    specialties: List[str] = Field(default_factory=list)
    source: Optional[str] = None

    class Config:
        validate_by_name = True

    @field_validator("latitude", "longitude")
    def check_bretagne_bounds(cls, value, info):
        """Check if charging station coords are in Bretagne"""
        BRETAGNE_BOUNDS = {
            "latitude_min": 47.0,
            "latitude_max": 48.9,
            "longitude_min": -5.2,
            "longitude_max": -1.0,
        }

        min_val = BRETAGNE_BOUNDS[f"{info.field_name}_min"]
        max_val = BRETAGNE_BOUNDS[f"{info.field_name}_max"]

        if not (min_val <= value <= max_val):
            raise ValueError(
                f"{info.field_name} {value} is out of Bretagne bounds "
                f"({min_val} - {max_val})"
            )
        return value

    @field_validator("power", mode="before")
    def normalize_power(cls, value):
        value_str = str(value)
        if not value_str:
            return "N/A"
        if not value_str.endswith("kW"):
            return f"{value_str}kW"
        return value_str

    @field_validator("name")
    def default_name(cls, value):
        return value or "Station de recharge"

    @field_validator("address")
    def default_address(cls, value):
        return value or "Adresse non disponible"
