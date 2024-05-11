"""
URL configuration for job_hunters app.
"""

from django.urls import path
from . import views

handler404 = "job_hunters.views.handler404"
handler500 = "job_hunters.views.handler500"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("jobs/", views.jobs_view, name="jobs"),
    path("job/", views.job_create_view, name="job_create"),
    path("jobs/<uuid:job_id>/", views.job_view, name="job"),
    path(
        "jobs/<uuid:job_id>/apply/",
        views.ApplicationWizardView.as_view(),
        name="job_apply",
    ),
    path("applications/", views.applications_view, name="applications"),
    path("company/<str:company_name>", views.company_details_view, name="company"),
]
