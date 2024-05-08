"""
This file contains the views for the job_hunters app.
"""

from base64 import b64encode
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from job_hunters.forms.login import LoginForm
from job_hunters.forms.profile import ProfileForm
from job_hunters.forms.register import RegisterForm

# Create your views here.


def index(request):
    """
    View for the index page.
    """

    if request.user.is_authenticated:
        return render(request, "index.html", {"user": request.user})

    return render(request, "index.html")


def register_view(request):
    """
    View for the register page.
    """

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, "register.html", {"form": form})

    form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    """
    View for the login page.
    """

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("profile")

        return render(request, "login.html", {"form": form})

    return render(request, "login.html")


def logout_view(request):
    """
    View for the logout page.
    """

    logout(request)

    return redirect("login")


def profile_view(request):
    """
    View for the profile page.
    """
    context = {
        "user": request.user
    }

    if hasattr(request.user, "companyprofile"):
        logo_image = request.user.companyprofile.logo_image
        cover_image = request.user.companyprofile.cover_image
        logo_b64 = b64encode(logo_image.image_data).decode("utf-8")
        cover_b64 = b64encode(cover_image.image_data).decode("utf-8")
        logo_encoded = f"data:image/png;base64,{logo_b64}"
        cover_encoded = f"data:image/png;base64,{cover_b64}"
        context["logo_data"] = logo_encoded
        context["cover_data"] = cover_encoded

    else:
        image = request.user.userprofile.profile_image
        image_b64 = b64encode(image.image_data).decode("utf-8")
        image_encoded = f"data:image/png;base64,{image_b64}"
        context["image_data"] = image_encoded


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("profile")

        context["form"] = form
        return render(request, "profile.html", context)

    return render(request, "profile.html", context)
