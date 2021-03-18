from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.seeds import seed as seeding_core


class Command(BaseCommand):
    help = 'Seed the database'

    def handle(self, *args, **options):

         #Admin User erstellen

        user = User.objects.filter(username='admin').first()
        if user is not None:
            print('Admin user exists')

        else:
            admin = User.objects.create_user(
            'admin',
            password='@12345678',
            )
            admin.is_superuser = True
            admin.is_staff = True
            admin.save()
            print('Create Admin User')
        seeding_core()
        return None