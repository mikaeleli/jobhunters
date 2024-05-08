"""
URL configuration for job_hunters app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("jobs/", views.jobs_view, name="jobs"),
    path("applications/", views.applications_view, name="applications"),
]
