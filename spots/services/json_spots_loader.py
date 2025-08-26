# spots/services/json_data_loader.py
import json
import logging
import os
from typing import Dict, List

from django.conf import settings

from ..mappers.json_mapper import JsonMapper
from ..models import Spot

logger = logging.getLogger(__name__)


class JsonSpotsLoader:
    """Service to load spots from static json data"""

    def __init__(self):
        self.data_dir = os.path.join(settings.BASE_DIR, "data")

    def get_all_static_spots(self) -> List[Spot]:
        raw_spots = []

        # Configurate files to load
        json_files = {
            "organic_markets.json": "markets",
            "bio_shops.json": "shops",
            "local_producers.json": "producers",
            "eco_accommodations.json": "accommodations",
        }

        for filename, key in json_files.items():
            try:
                spots = self._load_spots_from_file(filename, key)
                raw_spots.extend(spots)
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")

        return JsonMapper.to_spots(raw_spots)

    def _load_spots_from_file(self, filename: str, data_key: str) -> List[Dict]:
        file_path = os.path.join(self.data_dir, filename)

        if not os.path.exists(file_path):
            logger.warning(f"File not found: {filename}")
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(data_key, [])
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in file: {filename}")
            return []
        except Exception as e:
            logger.error(f"Error reading file {filename}: {e}")
            return []
