"""
Job application
"""

import uuid
from django.db import models


from .job import Job


class Application(models.Model):
    """
    Job application
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )
    full_name = models.CharField(max_length=255)
    cover_letter = models.TextField()
    street_name = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)


class Experience(models.Model):
    """
    Experience
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="experiences",
    )
    role = models.CharField(max_length=255)
    workplace_name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class Recommendation(models.Model):
    """
    Recommendation
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    can_be_contacted = models.BooleanField()
