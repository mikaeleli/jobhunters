"""
URL configuration for job_hunters app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
