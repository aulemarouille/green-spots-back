# spots/views.py
import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .services.spots_service import SpotsService

logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_all_spots(request):
    try:
        spots_service = SpotsService()
        spots = spots_service.get_all_spots()

        return JsonResponse(spots, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in get_all_spots view: {e}")
        return Response(
            {
                "error": "Internal server error",
                "message": "Failed to retrieve spots data",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def refresh_spots_cache(request):
    """
    Force le refresh du cache des spots
    (Utile pour debug ou refresh manuel)
    """
    try:
        spots_service = SpotsService()
        spots_service.clear_cache()

        return Response(
            {"message": "Cache cleared successfully"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return Response(
            {"error": "Failed to clear cache"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
