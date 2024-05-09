"""
Forms for the profile page.
"""

from django import forms
from job_hunters.models.image import Image


class ProfileForm(forms.Form):
    """
    Form for the profile page.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    full_name = forms.CharField(max_length=255, required=False)
    profile_image = forms.ImageField(required=False)
    company_name = forms.CharField(max_length=255, required=False)
    company_address = forms.CharField(max_length=255, required=False)
    company_logo = forms.ImageField(required=False)
    company_cover = forms.ImageField(required=False)
    company_description = forms.CharField(max_length=255, required=False)
    company_website = forms.URLField(required=False)

    def save(self):
        data = self.cleaned_data

        user = self.user

        changes = False
        if hasattr(user, "companyprofile"):
            if data.get("company_name") != user.companyprofile.name:
                user.companyprofile.name = data.get("company_name")
                changes = True

            if data.get("company_address") != user.companyprofile.address:
                user.companyprofile.address = data.get("company_address")
                changes = True

            if data.get("company_description") != user.companyprofile.description:
                user.companyprofile.description = data.get("company_description")
                changes = True

            if data.get("company_website") != user.companyprofile.webpage_url:
                user.companyprofile.webpage_url = data.get("company_website")
                changes = True

            if data.get("company_logo") is not None:
                if hasattr(user.companyprofile.logo, "image_data"):
                    user.companyprofile.logo_image.image_data = data.get("company_logo").read()

                else:
                    logo_image = Image.objects.create(
                        image_data = data.get("company_logo").read(),
                    )
                    user.companyprofile.logo_image = logo_image

                user.companyprofile.logo_image.save()
                changes = True

            if data.get("company_cover") is not None:
                if hasattr(user.companyprofile.cover_image, "image_data"):
                    user.companyprofile.cover_image.image_data = data.get("company_cover").read()

                else:
                    cover_image = Image.objects.create(
                        image_data=data.get("company_cover").read(),
                    )
                    user.companyprofile.cover_image = cover_image

                user.companyprofile.cover_image.save()
                changes = True

            if changes:
                user.companyprofile.save()

        else:
            if data.get("full_name") != user.userprofile.full_name:
                user.userprofile.full_name = data.get("full_name")
                changes = True

            if data.get("profile_image") is not None:
                if hasattr(user.userprofile.profile_image, "image_data"):
                    user.userprofile.profile_image.image_data = data.get("profile_image").read()

                else:
                    profile_image = Image.objects.create(
                        image_data=data.get("profile_image").read(),
                    )
                    user.userprofile.profile_image = profile_image

                user.userprofile.profile_image.save()
                changes = True

            if changes:
                user.userprofile.save()

        user.save()
