from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from job_hunters.models import CompanyProfile, UserProfile

class Command(BaseCommand):
    def handle(self, **options):
        print("Getting all usernames")
        print()
        print("Company users:")
        for company in CompanyProfile.objects.all():
            print(f"{company.user.username:>30} - {company.name}")
        print()
        print()
        print("Job seeking users:")
        for user in UserProfile.objects.all():
            print(f"{user.user.username:>30} - {user.full_name}")
