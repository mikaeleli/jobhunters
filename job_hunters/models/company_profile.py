"""
Company profile
"""

import uuid
from django.db import models
from django.contrib.auth.models import User

from .image import Image


class CompanyProfile(models.Model):
    """
    Company profile
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="companyprofile")
    address = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255)
    webpage_url = models.URLField()
    logo_image = models.OneToOneField(
        Image, on_delete=models.CASCADE, related_name="company_logo"
    )
    cover_image = models.OneToOneField(
        Image, on_delete=models.CASCADE, related_name="company_cover"
    )

    def __str__(self):
        return str(self.name)
