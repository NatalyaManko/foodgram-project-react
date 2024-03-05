import csv
import sqlite3

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient
from pathlib import Path


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, **options):

        path = (f'{Path(__file__).resolve().parent.parent.parent.parent.parent}'
               + '\data\ingredients.csv')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                        )
        except Exception:
            raise CommandError('Ошибка заполнения базы данных')
