"""
Forms for the create job page.
"""
import datetime
from typing import Any

from django import forms

from job_hunters.models import Job, Category


class JobForm(forms.Form):
    """
    Form for the create job page.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    job_title = forms.CharField(max_length=250, initial="", required=False)
    job_category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), to_field_name="id", required=False)
    job_due_date = forms.DateField(required=False)
    job_start_date = forms.DateField(required=False)
    job_is_part_time = forms.BooleanField(required=False)
    job_description = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        # check if job has title
        if cleaned_data.get("job_title") is None or cleaned_data.get("job_title") == "":
            self.add_error("job_title", "Job title is required")

        # check if job has valid category
        if cleaned_data.get("job_category") is None:
            self.add_error("job_category", "Job category is required")

        # check if job has a valid due date
        if cleaned_data.get("job_due_date") is None:
            self.add_error("job_due_date", "Job due date is required")

        elif cleaned_data.get("job_due_date") < datetime.date.today():
            self.add_error("job_due_date", "Job due date has to be a future date")

        if cleaned_data.get("job_start_date") is None:
            self.add_error("job_start_date", "Job start date is required")

        elif cleaned_data.get("job_start_date") < datetime.date.today():
            self.add_error("job_start_date", "Job start date has to be a future date")

        if cleaned_data.get("job_description") is None or cleaned_data.get("job_description") == "":
            self.add_error("job_description", "Job description is required")

        return cleaned_data

    def save(self):
        data = self.cleaned_data

        user = self.user

        job = Job.objects.create(
            offered_by=user.companyprofile,
            title=data.get("job_title"),
            due_date=data.get("job_due_date"),
            starting_date=data.get("job_start_date"),
            is_part_time=data.get("job_is_part_time"),
            description=data.get("job_description"),
        )

        job.categories.set(data.get("job_category"))
        
        job.save()
        
        return job