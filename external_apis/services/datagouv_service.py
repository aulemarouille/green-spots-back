# external_apis/services/datagouv_service.py
import concurrent.futures
import logging
from typing import Dict, List, Optional

import requests

from spots.mappers.charging_station_mapper import ChargingStationMapper
from spots.models import Spot

logger = logging.getLogger(__name__)


class DatagouvService:
    """
    Service to get all charging station in Bretagne from data.gouv.fr
    """

    def __init__(self):
        self.base_url = "https://tabular-api.data.gouv.fr/api/resources/eb76d20a-8501-400e-b336-d85724de5435/data/"
        self.session = requests.Session()
        self.session.timeout = 15
        self.breizh_departments = [22, 29, 35, 56]

    def fetch_charging_stations(self) -> List[Spot]:
        all_stations = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_dept = {
                executor.submit(self._fetch_stations_by_department, dept): dept
                for dept in self.breizh_departments
            }

            for future in concurrent.futures.as_completed(future_to_dept):
                dept = future_to_dept[future]
                try:
                    stations = future.result()
                    all_stations.extend(stations)
                except Exception as e:
                    logger.error(f"Failed to fetch stations for department {dept}: {e}")

        return all_stations

    def _fetch_stations_by_department(self, department: int) -> List[Spot]:
        """Get all charging stations from one department"""
        params = self._build_request_params()
        params["adresse_station__contains"] = f", {department}"

        response_stations = self._make_request(params)

        if response_stations and "data" in response_stations:
            return ChargingStationMapper.to_spots(response_stations["data"])

        return []

    def _build_request_params(self) -> Dict:
        return {
            "columns": "adresse_station,coordonneesXY,nbre_pdc,nom_station,puissance_nominale",
            "puissance_nominale__differs": 0,
            "page": 0,
            "page_size": 50,
        }

    def _make_request(self, params: Dict) -> Optional[Dict]:
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"API request failed: {e}")
            return None

    def close(self):
        if self.session:
            self.session.close()
