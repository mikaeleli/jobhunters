"""
Forms for the register page.
"""

from typing import Any

from django import forms
from django.contrib.auth.models import User

from job_hunters.models import UserProfile, CompanyProfile
from job_hunters.models.image import Image


class RegisterForm(forms.Form):
    """
    Form for the register page.
    """

    user_type = forms.ChoiceField(widget=forms.Select(), choices=([('jobseeker', 'jobseeker'), ('company', 'company')]))
    full_name = forms.CharField(max_length=255, initial="", required=False)
    company_name = forms.CharField(max_length=255, initial="", required=False)
    email = forms.EmailField(initial="")
    password = forms.CharField(max_length=255, initial="")
    confirm_password = forms.CharField(max_length=255, initial="")
    profile_image = forms.ImageField(required=False)
    company_logo = forms.ImageField(required=False)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if cleaned_data.get("user_type") == "company":
            # check if company logo is uploaded
            if self.files.get("company_logo") is None:
                self.add_error("company_logo", "Company logo is required")

        if cleaned_data.get("user_type") == "jobseeker":
            # check if profile image is uploaded
            if self.files.get("profile_image") is None:
                self.add_error("profile_image", "Profile image is required")

        # check if email already exists
        if User.objects.filter(email=cleaned_data.get("email")).exists():
            self.add_error("email", "Email already exists")

        # check if passwords match
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("password", "Passwords do not match")
            self.add_error("confirm_password", "Passwords do not match")

        return cleaned_data

    def save(self):
        data = self.cleaned_data

        user = User.objects.create_user(
            email=data.get("email"),
            username=data.get("email")
        )
        print('test');
        if data.get('user_type') == "company":
            company_logo = Image.objects.create(
                image_data=data.get("company_logo").read(),
            )
            company_profile = CompanyProfile.objects.create(
                user=user,
                name=data.get("company_name"),
                logo_image=company_logo,
            )
            user.set_password(data.get("password"))
            user.save()
            return company_profile

        elif data.get('user_type') == "jobseeker":
            print('jobseeker')
            profile_image = Image.objects.create(
                image_data=data.get("profile_image").read(),
            )
            user_profile = UserProfile.objects.create(
                user=user,
                full_name=data.get("full_name"),
                profile_image=profile_image,
            )
            user.set_password(data.get("password"))
            user.save()
            return user_profile




