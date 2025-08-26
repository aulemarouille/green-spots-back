# spots/mappers/json_mapper.py
import logging
from typing import Dict, List

from pydantic import ValidationError

from ..models import Spot

logger = logging.getLogger(__name__)


class JsonMapper:
    @classmethod
    def to_spots(cls, raw_spots: List[Dict]) -> List[Spot]:
        spots = []

        for raw_spot in raw_spots:
            try:
                spot = Spot(**raw_spot)
                spots.append(spot)
            except ValidationError as e:
                logger.warning(f"Invalid JSON spot: {e}")

        return spots
