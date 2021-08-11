import csv

from internships.models import Country, Language

from django.conf import settings


def fill_languages():
    """Fill Default Languages"""
    languages = []
    initial_dir = settings.BASE_DIR.joinpath('initial')
    with open(initial_dir.joinpath('languages.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            languages.append(row.pop().strip())

    Language.objects.bulk_create(
        [Language(name=lang) for lang in languages],
        ignore_conflicts=True
    )



def fill_countries():
    """Fill Default Countries"""
    countries = []
    initial_dir = settings.BASE_DIR.joinpath('initial')
    with open(initial_dir.joinpath('countries.csv')) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            countries.append(row.pop().strip())
    Country.objects.bulk_create(
        [Language(name=country) for country in countries],
        ignore_conflicts=True
    )