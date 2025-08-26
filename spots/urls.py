# spots/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("spots/", views.get_all_spots, name="get_all_spots"),
]
