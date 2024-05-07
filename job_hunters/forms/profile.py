"""
Forms for the profile page.
"""

from django import forms


class ProfileForm(forms.Form):
    """
    Form for the profile page.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    profile_image = forms.ImageField(required=False)

    def save(self):
        data = self.cleaned_data

        user = self.user

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")

        if data.get("profile_image") is not None:
            user.userprofile.profile_image.image_data = data.get("profile_image").read()
            user.userprofile.profile_image.save()

        user.save()
