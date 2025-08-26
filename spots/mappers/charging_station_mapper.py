# spots/mappers/charging_station_mapper.py
import logging
from typing import Dict, List, Optional, Set, Tuple

from ..models import Spot, SpotType

logger = logging.getLogger(__name__)


class ChargingStationMapper:
    """Map raw charging stations data from data.gouv in Spot"""

    @classmethod
    def to_spots(cls, raw_stations: List[Dict]) -> List[Spot]:
        mapped_stations: List[Spot] = []
        locations = set()

        for raw_station in raw_stations:
            try:
                spot = cls._to_spot(raw_station)
                if spot and cls._is_unique_location(spot, locations):
                    mapped_stations.append(spot)
                    cls._add_location(spot, locations)
            except Exception as e:
                logger.warning(f"Error mapping station: {e}")

        return mapped_stations

    @classmethod
    def _to_spot(cls, raw_station: Dict) -> Optional[Spot]:
        coords = raw_station.get("coordonneesXY", [])
        if not (isinstance(coords, list) and len(coords) >= 2):
            return None

        try:
            lon = float(coords[0])  # first = longitude
            lat = float(coords[1])  # second = latitude
        except (ValueError, TypeError):
            return None

        station = {
            "name": raw_station.get("nom_station"),
            "type": SpotType.CHARGING_STATION,
            "latitude": lat,
            "longitude": lon,
            "address": raw_station.get("adresse_station"),
            "description": cls._build_description(raw_station),
            "power": raw_station.get("puissance_nominale"),
            "source": "data.gouv.fr IRVE",
        }

        return Spot(**station)

    @classmethod
    def _build_description(cls, raw_station: Dict) -> str:
        power = raw_station.get("puissance_nominale", "N/A")
        connectors = raw_station.get("nbre_pdc", 1)
        return f"Station de recharge {power}kW - {connectors} place(s)"

    # Manage duplication
    @classmethod
    def _is_unique_location(cls, station: Spot, locations: Set) -> bool:
        """Check if is unique location to delete duplication"""
        coord_key = cls._get_coordinate_key(station)
        return coord_key not in locations

    @classmethod
    def _add_location(cls, station: Spot, locations: Set) -> None:
        coord_key = cls._get_coordinate_key(station)
        locations.add(coord_key)

    @classmethod
    def _get_coordinate_key(cls, station: Spot) -> Tuple[float, float]:
        """Create unique key based on coords"""
        return (
            round(station.latitude, 6),
            round(station.longitude, 6),
        )
