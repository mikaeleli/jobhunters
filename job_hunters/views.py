"""
This file contains the views for the job_hunters app.
"""

import datetime

from base64 import b64encode
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from job_hunters.middleware.login_required_middleware import login_exempt
from formtools.wizard.views import SessionWizardView

from job_hunters.forms.job_create import JobForm
from job_hunters.forms.jobs_filter import JobsFilter
from job_hunters.forms.login import LoginForm
from job_hunters.forms.profile import ProfileForm
from job_hunters.forms.register import RegisterForm
from job_hunters.forms.job_application import (
    ContactInformationForm,
    CoverLetterForm,
    ExperienceForm,
    RecommendationForm,
    ReviewForm,
)
from job_hunters.models import (
    Job,
    CompanyProfile,
    Category,
    Application,
    Experience,
    Recommendation,
)


# Create your views here.


@login_exempt
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
    context = {"user": request.user, "userprofile": False, "companyprofile": False}

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
        context["company_jobs"] = Job.objects.filter(
            offered_by=request.user.companyprofile, due_date__gte=datetime.date.today()
        )
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


@login_exempt
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

            return render(
                request,
                "jobs.html",
                {"jobs": jobs, "form": form, "user_is_company": user_is_company},
            )

        return render(
            request,
            "jobs.html",
            {"jobs": jobs, "form": form, "user_is_company": user_is_company},
        )

    form = JobsFilter(categories=categories, companies=companies)
    jobs = Job.objects.all()

    return render(
        request,
        "jobs.html",
        {"jobs": jobs, "form": form, "user_is_company": user_is_company},
    )


APPLICATION_FORMS = [
    ("contact_information", "Contact Information", ContactInformationForm),
    ("cover_letter", "Cover letter", CoverLetterForm),
    ("experience", "Experience", ExperienceForm),
    ("recommendation", "Recommendations", RecommendationForm),
    ("review", "Review", ReviewForm),
]

APPLICATION_FORM_TEMPLATES = {
    "contact_information": "job_application/contact_information.html",
    "cover_letter": "job_application/cover_letter.html",
    "experience": "job_application/experience.html",
    "recommendation": "job_application/recommendation.html",
    "review": "job_application/review.html",
}


class ApplicationWizardView(SessionWizardView):
    form_list = [form for _, _, form in APPLICATION_FORMS]

    def get_template_names(self):
        name, _, _ = APPLICATION_FORMS[int(self.steps.current)]

        return APPLICATION_FORM_TEMPLATES[name]

    def get_form_prefix(self, step=None, form=None):
        if not step:
            step = self.steps.current

        form = APPLICATION_FORMS[int(step)][2]

        return form.prefix

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)

        context["job"] = Job.objects.get(id=self.kwargs["job_id"])

        context["title"] = APPLICATION_FORMS[int(self.steps.current)][1]

        context["nav_list"] = []

        for i, (name, title, _) in enumerate(APPLICATION_FORMS):
            context["nav_list"].append(
                {
                    "name": name,
                    "title": title,
                    "is_current": i == int(self.steps.current),
                    "step": i,
                }
            )

        extra_data = self.storage.extra_data

        if "experience" in extra_data:
            raw_data = extra_data["experience"]
            experience_data = []

            # deserialize the data, converting date strings to date objects
            for data in raw_data:
                experience_data.append(
                    {
                        "role": data["role"],
                        "company": data["company"],
                        "start_date": data["start_date"],
                        "end_date": data["end_date"] if "end_date" in data else None,
                    }
                )

            experience_data.sort(
                key=lambda x: (
                    x["end_date"]
                    if x["end_date"] is not None
                    else datetime.datetime.max.date()
                ),
                reverse=True,
            )

            context["experience_data"] = experience_data

        if "recommendations" in extra_data:
            raw_data = extra_data["recommendations"]
            recommendation_data = []

            for data in raw_data:
                recommendation_data.append(
                    {
                        "name": data["name"],
                        "role": data["role"],
                        "company": data["company"],
                        "email": data["email"],
                        "phone": data["phone"],
                        "can_be_contacted": data["can_be_contacted"],
                    }
                )

            context["recommendation_data"] = recommendation_data

        if form.prefix == "review":
            contact_information = self.get_cleaned_data_for_step("0")
            cover_letter = self.get_cleaned_data_for_step("1")

            if contact_information:
                context["contact_information"] = contact_information
            if cover_letter:
                context["cover_letter"] = cover_letter.get("cover_letter", "")

        return context

    def post(self, *args, **kwargs):
        current_form = APPLICATION_FORMS[int(self.steps.current)][2]

        # if it's a navigation request, fallback to the default behavior
        if "wizard_goto_step" in self.request.POST:
            return super().post(*args, **kwargs)

        if current_form.prefix == "experience":
            request = args[0]

            current_form = current_form(request.POST)

            if current_form.has_required_data():
                extra_data = self.storage.extra_data

                if "experience" not in extra_data:
                    extra_data["experience"] = []

                # json serialize the form data, then append it to the list
                serialized_data = {
                    "role": current_form.cleaned_data["role"],
                    "company": current_form.cleaned_data["company"],
                    "start_date": str(current_form.cleaned_data["start_date"]),
                }

                if current_form.cleaned_data["end_date"] is not None:
                    serialized_data["end_date"] = str(
                        current_form.cleaned_data["end_date"]
                    )

                extra_data["experience"].append(serialized_data)

                self.storage.extra_data = extra_data

                # clear current step data, since we don't want to prefill
                # the form after a successful submission
                self.storage.set_step_data(self.steps.current, {})

                return self.render(self.get_form(self.steps.current, data={}))

            # if the form is not valid, render the form again with the errors
            return super().post(*args, **kwargs)

        if current_form.prefix == "recommendation":
            request = args[0]

            current_form = current_form(request.POST)

            if current_form.has_required_data():
                extra_data = self.storage.extra_data

                if "recommendations" not in extra_data:
                    extra_data["recommendations"] = []

                # json serialize the form data, then append it to the list
                serialized_data = {
                    "name": current_form.cleaned_data["name"],
                    "role": current_form.cleaned_data["role"],
                    "company": current_form.cleaned_data["company"],
                    "email": current_form.cleaned_data["email"],
                    "phone": current_form.cleaned_data["phone"],
                    "can_be_contacted": current_form.cleaned_data["can_be_contacted"],
                }

                extra_data["recommendations"].append(serialized_data)

                self.storage.extra_data = extra_data

                # clear current step data, since we don't want to prefill
                # the form after a successful submission
                self.storage.set_step_data(self.steps.current, {})

                return self.render(self.get_form(self.steps.current, data={}))

            # if the form is not valid, render the form again with the errors
            return super().post(*args, **kwargs)

        # if it's not a form that requires special handling, fallback to the default behavior
        return super().post(*args, **kwargs)

    def done(self, form_list, **kwargs):
        job = Job.objects.get(id=self.kwargs["job_id"])

        contact_information = form_list[0].cleaned_data
        cover_letter = form_list[1].cleaned_data["cover_letter"]

        application = Application.objects.create(
            job=job,
            applicant=self.request.user,
            full_name=contact_information["full_name"],
            cover_letter=cover_letter,
            street_name=contact_information["street_name"],
            house_number=contact_information["house_number"],
            city=contact_information["city"],
            postal_code=contact_information["postal_code"],
            country=contact_information["country"],
        )

        for experience in self.storage.extra_data.get("experience", []):
            Experience.objects.create(
                application=application,
                role=experience["role"],
                workplace_name=experience["company"],
                start_date=experience["start_date"],
                end_date=experience["end_date"],
            )

        for recommendation in self.storage.extra_data.get("recommendations", []):
            Recommendation.objects.create(
                application=application,
                name=recommendation["name"],
                email=recommendation["email"],
                phone_number=recommendation["phone"],
                role=recommendation["role"],
                can_be_contacted=recommendation["can_be_contacted"],
            )

        context = {
            "job_title": job.title,
            "company_name": job.offered_by.name,
        }

        return render(self.request, "job_application/success.html", context)


@login_exempt
def job_view(request, job_id):
    """
    View for the job page.
    """

    job = Job.objects.get(id=job_id)
    company_logo_image = job.offered_by.logo_image
    company_logo_b64 = b64encode(company_logo_image.image_data).decode("utf-8")
    company_logo_data_encoded = f"data:image/png;base64,{company_logo_b64}"

    user_is_company = bool(
        request.user.is_authenticated and hasattr(request.user, "companyprofile")
    )

    application = None
    if request.user.is_authenticated and not user_is_company:
        matching_applications = Application.objects.filter(applicant=request.user, job=job)
        if matching_applications.count() > 0:
            application = matching_applications.first()

    return render(
        request,
        "job_details.html",
        {
            "job": job,
            "company_logo_data": company_logo_data_encoded,
            "application": application,
            "user_is_company": user_is_company,
        },
    )


def job_create_view(request):
    """
    View for the job create page.
    """
    company_jobs = None
    if request.user.is_authenticated and hasattr(request.user, "companyprofile"):
        company_jobs = Job.objects.filter(
            offered_by=request.user.companyprofile, due_date__gte=datetime.date.today()
        )

    if (
        request.method == "POST"
        and request.user.is_authenticated
        and hasattr(request.user, "companyprofile")
    ):
        form = JobForm(request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect("jobs")

        return render(
            request,
            "job_create.html",
            {
                "company": request.user.companyprofile,
                "job_categories": Category.objects.all(),
                "company_jobs": company_jobs,
                "form": form,
            },
        )

    if request.user.is_authenticated and hasattr(request.user, "companyprofile"):
        return render(
            request,
            "job_create.html",
            {
                "company": request.user.companyprofile,
                "job_categories": Category.objects.all(),
                "company_jobs": company_jobs,
            },
        )

    return redirect("jobs")


@login_exempt
def company_details_view(request, company_name):
    """
    View for the company details page.
    """
    company_name = company_name.replace("_", " ")
    company = CompanyProfile.objects.filter(name__iexact=company_name).first()
    company_jobs = Job.objects.filter(
        offered_by=company, due_date__gte=datetime.date.today()
    )

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
    is_company = False
    applications = Application.objects.none()
    if hasattr(request.user, "userprofile"):
        applications = request.user.applications.all()

    elif hasattr(request.user, "companyprofile"):
        jobs = Job.objects.filter(offered_by=request.user.companyprofile)
        applications = Application.objects.none()
        for job in jobs:
            applications |= job.applications.all()
        is_company = True

    return render(
        request,
        "applications.html",
        {"applications": applications, "is_company": is_company},
    )


@login_exempt
def handler404(request, exception, template_name="404.html"):
    response = render(request, template_name, exception)
    response.status_code = 404
    return response


@login_exempt
def handler500(request, *args):
    return render(request, "500.html", status=500)
