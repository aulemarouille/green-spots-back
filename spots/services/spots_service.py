# spots/services/spots_service.py
import logging
from typing import Dict, List

from django.core.cache import cache
from external_apis.services.datagouv_service import DatagouvService

from .json_spots_loader import JsonSpotsLoader

logger = logging.getLogger(__name__)


class SpotsService:
    """Main service to manage all eco spots"""

    # Cache keys
    CHARGING_STATIONS_CACHE_KEY = "charging_stations"
    CACHE_TIMEOUT = 3600 * 24  # 24h

    def __init__(self):
        self.datagouv_service = DatagouvService()
        self.json_loader = JsonSpotsLoader()

        self.static_spots = [
            spot.model_dump(mode="json")
            for spot in self.json_loader.get_all_static_spots()
        ]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.datagouv_service.close()

    def get_all_spots(self) -> Dict:
        """
        Get all static spots and charging stations from data.gouv
        """
        try:
            charging_stations = self._get_charging_stations()
            static_spots = self._get_static_spots()
            all_spots = charging_stations + static_spots

            return self._build_response(all_spots)

        except Exception as e:
            logger.error(f"Failed to get spots: {e}")
            return self._build_error_response()

    def _get_charging_stations(self) -> List[Dict]:
        """
        Get charging stations with cache
        """
        cached_stations = cache.get(self.CHARGING_STATIONS_CACHE_KEY)

        if cached_stations is not None:
            return cached_stations

        try:
            stations = self.datagouv_service.fetch_charging_stations()
            json_stations = [station.model_dump() for station in stations]

            cache.set(
                self.CHARGING_STATIONS_CACHE_KEY,
                json_stations,
                self.CACHE_TIMEOUT,
            )

            return json_stations

        except Exception as e:
            logger.error(f"Failed to fetch charging stations: {e}")
            return []

    def _get_static_spots(self) -> List[Dict]:
        return self.static_spots

    def _build_response(self, spots: List[Dict]) -> Dict:
        type_counts = {}
        for spot in spots:
            spot_type = spot.get("type", "unknown")
            type_counts[spot_type] = type_counts.get(spot_type, 0) + 1

        return {
            "spots": spots,
            "total_count": len(spots),
            "types": list(type_counts.keys()),
            "type_counts": type_counts,
            "region": "Bretagne",
            "sources": ["data.gouv.fr IRVE", "Static JSON data"],
        }

    def _build_error_response(self) -> Dict:
        return {
            "spots": [],
            "total_count": 0,
            "types": [],
            "type_counts": {},
            "region": "Bretagne",
            "sources": [],
            "error": "Failed to retrieve spots data",
        }
