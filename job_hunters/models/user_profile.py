"""
User profile
"""

import uuid
from django.db import models
from django.contrib.auth.models import User

from .image import Image


class UserProfile(models.Model):
    """
    User profile
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.OneToOneField(
        Image, on_delete=models.CASCADE, related_name="profile_image"
    )

    def __str__(self):
        return str(self.user)
