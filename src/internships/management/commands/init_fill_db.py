from django.core.management.base import BaseCommand

from internships.services.init_fill_db import fill_languages, fill_countries


class Command(BaseCommand):
    help = 'Initial fill database'

    def handle(self, *args, **options):
        fill_languages()
        fill_countries()