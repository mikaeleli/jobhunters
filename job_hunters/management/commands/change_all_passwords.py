from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Change all users passwords'

    def add_arguments(self, parser):
        parser.add_argument("new_password", nargs="+", type=str, help="New password")
    def handle(self, **options):
        try:
            new_password = options["new_password"][0]
            if (input(f'This is super dangerous and will set all passwords to a "{new_password}", continue? (y/n) ')
                    .lower() == 'y'):
                # set all users passwords
                all_users = User.objects.all()
                for user in all_users:
                    user.set_password(new_password)
                    user.save()

        except Exception as e:
            print('Please provide a new password as an argument.', e)
