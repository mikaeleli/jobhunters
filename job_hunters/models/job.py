"""
Job
"""

import datetime
import uuid
from django.db import models
from django.urls import reverse

from .company_profile import CompanyProfile
from .category import Category


class Job(models.Model):
    """
    Job
    """

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=255)
    is_part_time = models.BooleanField()
    posted_date = models.DateTimeField(default=datetime.datetime.now)
    due_date = models.DateTimeField()
    starting_date = models.DateTimeField()
    description = models.TextField()
    offered_by = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    categories = models.ManyToManyField(
        Category,
        related_name="jobs",
    )

    def get_absolute_url(self):
        return reverse("job",args=[str(self.id),])

    def __str__(self):
        return str(self.title)
