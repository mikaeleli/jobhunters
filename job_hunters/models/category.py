"""
Category model
"""

import uuid
from django.db import models


class Category(models.Model):
    """
    Defines a category for a job posting
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
