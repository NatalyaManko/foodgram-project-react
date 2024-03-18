import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from ingredients.models import Ingredient, Unit


class Command(BaseCommand):
    """Команда для загрузки данных из csv-файлов в базу данных."""

    help = 'Load ingredients and measurement units data from .csv to DB'

    def handle(self, *args, **options):

        filename = 'ingredients.csv'
        with open(f'{options["path"]}/{filename}', encoding='utf-8') as f:
            reader = csv.reader(f)
            for ingredient_name, unit_name in reader:
                unit, status = Unit.objects.get_or_create(name=unit_name)
                Ingredient.objects.get_or_create(name=ingredient_name,
                                                 measurement_unit=unit)

        return True

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default=str(settings.BASE_DIR) + '/initial_data',
            help='Path to .csv files',
        )
