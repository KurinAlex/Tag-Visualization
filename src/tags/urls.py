"""
URL configuration for application
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
