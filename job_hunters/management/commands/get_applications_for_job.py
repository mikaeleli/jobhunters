from django.core.management.base import BaseCommand

from job_hunters.models import Job, Application

class Command(BaseCommand):
    help = 'Get the id of all applications for a specific job'

    def add_arguments(self, parser):
        parser.add_argument("job", nargs="+", type=str, help="Job id")
    def handle(self, **options):
        try:
            job_id = options["job"][0]
            job = Job.objects.get(id=job_id)
            for application in Application.objects.filter(job=job):
                print(f"Application: {str(application.id):>30}  Name: {application.applicant.userprofile.full_name:>30}")

        except Exception as e:
            print('Error.', e)
