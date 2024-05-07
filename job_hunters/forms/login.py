"""
Forms for the login page.
"""

from typing import Any
from django import forms

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    Form for the login page.
    """

    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        # check if email exists
        if not User.objects.filter(email=cleaned_data.get("email")).exists():
            self.add_error("email", "Either the email or password is incorrect")

        user = User.objects.get(email=cleaned_data.get("email"))

        # check if user is active
        if not user.is_active:
            self.add_error("email", "Either the email or password is incorrect")

        # check if password is correct
        password = cleaned_data.get("password")
        if not user.check_password(password):
            self.add_error("email", "Either the email or password is incorrect")

        return cleaned_data
