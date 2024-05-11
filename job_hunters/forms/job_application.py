"""
Forms for the job application.
"""

from typing import Any
from django import forms


class ContactInformationForm(forms.Form):
    """
    Form for the contact information.
    """

    prefix = "contact_information"

    full_name = forms.CharField(max_length=255, initial="")
    street_name = forms.CharField(max_length=255, initial="")
    house_number = forms.CharField(max_length=50, initial="")
    city = forms.CharField(max_length=255, initial="")
    postal_code = forms.CharField(max_length=50, initial="")
    country = forms.CharField(max_length=255, initial="")


class CoverLetterForm(forms.Form):
    """
    Form for the cover letter.
    """

    prefix = "cover_letter"

    cover_letter = forms.CharField(label="Cover Letter", required=False)


class ExperienceForm(forms.Form):
    """
    Form for past job experiences.
    """

    prefix = "experience"

    role = forms.CharField(label="Role", max_length=255)
    company = forms.CharField(label="Company", max_length=255)
    start_date = forms.DateField(label="Start Date")
    end_date = forms.DateField(label="End Date", required=False)

    def is_valid(self) -> bool:
        if self.has_changed():
            return super().is_valid()

        return True

    def has_required_data(self) -> bool:
        required_fields = ["role", "company", "start_date"]

        return (
            self.is_valid()
            and hasattr(self, "cleaned_data")
            and all(self.cleaned_data.get(field) for field in required_fields)
        )

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date > end_date:
            self.add_error("start_date", "Start date must be before end date")
            self.add_error("end_date", "End date must be after start date")

        return cleaned_data


class RecommendationForm(forms.Form):
    """
    Form for the recommendation.
    """

    prefix = "recommendation"

    name = forms.CharField(max_length=255)
    role = forms.CharField(max_length=255)
    company = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=50)
    can_be_contacted = forms.BooleanField(required=False)

    def is_valid(self) -> bool:
        if self.has_changed():
            return super().is_valid()

        return True

    def has_required_data(self) -> bool:
        required_fields = ["name", "role", "company", "email", "phone"]

        return (
            self.is_valid()
            and hasattr(self, "cleaned_data")
            and all(self.cleaned_data.get(field) for field in required_fields)
        )


class ReviewForm(forms.Form):
    """
    Form for the review.
    """

    prefix = "review"
