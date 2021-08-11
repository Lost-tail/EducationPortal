from django.core.management.base import BaseCommand

from internships.services.services import check_internships


class Command(BaseCommand):
    help = 'Check internships'

    def handle(self, *args, **options):
        check_internships()