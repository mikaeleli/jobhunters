"""
Forms for the register page.
"""

from typing import Any

from django import forms
from django.contrib.auth.models import User

from job_hunters.models import UserProfile
from job_hunters.models.image import Image


class RegisterForm(forms.Form):
    """
    Form for the register page.
    """

    full_name = forms.CharField(max_length=255, initial="")
    email = forms.EmailField(initial="")
    password = forms.CharField(max_length=255, initial="")
    confirm_password = forms.CharField(max_length=255, initial="")
    profile_image = forms.ImageField()

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

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

        profile_image = Image.objects.create(
            image_data=data.get("profile_image").read(),
        )

        user = User.objects.create_user(
            email=data.get("email"),
            username=data.get("email")
        )
        user.set_password(data.get("password"))
        user.save()

        user_profile = UserProfile.objects.create(
            user=user,
            full_name=data.get("full_name"),
            profile_image=profile_image,
        )

        return user_profile
