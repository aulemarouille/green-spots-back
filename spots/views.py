# spots/views.py
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from .services.spots_service import SpotsService

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_all_spots(request):
    with SpotsService() as service:
        spots = service.get_all_spots()
        return JsonResponse(spots, status=status.HTTP_200_OK)
