"""
URL configuration for config project.
"""

from django.urls import include, path

urlpatterns = [
    path("", include("tags.urls")),
]
