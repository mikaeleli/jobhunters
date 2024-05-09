"""
This file contains the views for the job_hunters app.
"""
import datetime
from base64 import b64encode
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from job_hunters.forms.job_create import JobForm
from job_hunters.forms.jobs_filter import JobsFilter
from job_hunters.forms.login import LoginForm
from job_hunters.forms.profile import ProfileForm
from job_hunters.forms.register import RegisterForm
from job_hunters.models import Job, CompanyProfile, Category

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
        "user": request.user,
        "userprofile": False,
        "companyprofile": False

    }

    if hasattr(request.user, "companyprofile"):
        logo_image = request.user.companyprofile.logo_image
        logo_b64 = b64encode(logo_image.image_data).decode("utf-8")
        logo_encoded = f"data:image/png;base64,{logo_b64}"
        if request.user.companyprofile.cover_image is not None:
            cover_image = request.user.companyprofile.cover_image
            cover_b64 = b64encode(cover_image.image_data).decode("utf-8")
            cover_encoded = f"data:image/png;base64,{cover_b64}"
            context["cover_data"] = cover_encoded

        context["logo_data"] = logo_encoded
        context["company_jobs"] = Job.objects.filter(offered_by=request.user.companyprofile, due_date__gte=datetime.date.today())
        context["companyprofile"] = True

    else:
        image = request.user.userprofile.profile_image
        image_b64 = b64encode(image.image_data).decode("utf-8")
        image_encoded = f"data:image/png;base64,{image_b64}"
        context["image_data"] = image_encoded
        context["userprofile"] = True

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("profile")

        context["form"] = form
        return render(request, "profile.html", context)

    return render(request, "profile.html", context)


def jobs_view(request):
    """
    View for the jobs page.
    """
    user_is_company = False
    if request.user.is_authenticated and hasattr(request.user, "companyprofile"):
        user_is_company = True

    categories = Category.objects.all()
    companies = CompanyProfile.objects.all()

    if request.method == "POST":
        form = JobsFilter(request.POST, categories=categories, companies=companies)
        jobs = Job.objects.all()

        if form.is_valid():
            search = form.cleaned_data.get("search")
            category = form.cleaned_data.get("category")
            company = form.cleaned_data.get("company")
            include_applied = form.cleaned_data.get("include_applied")
            order_by = form.cleaned_data.get("order_by")

            filters = {}

            if search:
                filters["title__icontains"] = search

            if category:
                filters["categories__name"] = category

            if company:
                filters["offered_by__name"] = company

            jobs = jobs.filter(**filters)

            if not include_applied:
                jobs = jobs.exclude(applications__applicant=request.user)

            if order_by:
                jobs = jobs.order_by(order_by)

            return render(request, "jobs.html", {"jobs": jobs, "form": form, "user_is_company": user_is_company})

        return render(request, "jobs.html", {"jobs": jobs, "form": form, "user_is_company": user_is_company})

    form = JobsFilter(categories=categories, companies=companies)
    jobs = Job.objects.all()

    return render(request, "jobs.html", {"jobs": jobs, "form": form, "user_is_company": user_is_company})


def job_view(request, job_id):
    """
    View for the job page.
    """

    job = Job.objects.get(id=job_id)

    return render(request, "job_details.html", {"job": job})


def job_apply_view(request, job_id):
    """
    View for the job apply page.
    """

    # TODO: Implement job application logic.

    return redirect("jobs")

def job_create_view(request):
    """
    View for the job create page.
    """

    company_jobs = Job.objects.filter(offered_by=request.user.companyprofile, due_date__gte=datetime.date.today())
    if request.method == "POST" and request.user.is_authenticated and hasattr(request.user, "companyprofile"):
        form = JobForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("jobs")

        return render(request, "job_create.html", {"company": request.user.companyprofile, "job_categories": Category.objects.all(), "company_jobs": company_jobs, "form": form})

    if request.user.is_authenticated and hasattr(request.user, "companyprofile"):
        return render(request, "job_create.html", {"company": request.user.companyprofile, "job_categories": Category.objects.all(), "company_jobs": company_jobs})

    return redirect("jobs")



def company_details_view(request, company_name):
    """
    View for the company details page.
    """
    company_name = company_name.replace("_", " ")
    company = CompanyProfile.objects.filter(name__iexact=company_name).first()
    company_jobs = Job.objects.filter(offered_by=company, due_date__gte=datetime.date.today())

    context = {
        "company": company,
        "company_jobs": company_jobs,
    }

    logo_image = company.logo_image
    logo_b64 = b64encode(logo_image.image_data).decode("utf-8")
    logo_encoded = f"data:image/png;base64,{logo_b64}"
    if company.cover_image is not None:
        cover_image = company.cover_image
        cover_b64 = b64encode(cover_image.image_data).decode("utf-8")
        cover_encoded = f"data:image/png;base64,{cover_b64}"
        context["cover_data"] = cover_encoded

    context["logo_data"] = logo_encoded

    if not company:
        raise Http404("Company not found")

    return render(request, "company_details.html", context)


def applications_view(request):
    """
    View for the applications page.
    """

    applications = request.user.applications.all()

    return render(request, "applications.html", {"applications": applications})

def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name, exception)
    response.status_code = 404
    return response

def handler500(request, *args, **argv):
    return render(request, '500.html', status=500)
