import csv
<<<<<<< HEAD
<<<<<<< HEAD
from pathlib import Path
=======
import sqlite3
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
import sqlite3
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient
<<<<<<< HEAD
<<<<<<< HEAD
=======
from pathlib import Path
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
from pathlib import Path
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3


class Command(BaseCommand):
    help = 'Заполняет базу данных из файлов CSV'

    def handle(self, *args, **options):

<<<<<<< HEAD
<<<<<<< HEAD
        path = (
            f'{Path(__file__).resolve().parent.parent.parent.parent}'
            + '/data/ingredients.csv'
        )
=======
        path = (f'{Path(__file__).resolve().parent.parent.parent.parent.parent}'
               + '\data\ingredients.csv')
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
        path = (f'{Path(__file__).resolve().parent.parent.parent.parent.parent}'
               + '\data\ingredients.csv')
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    Ingredient.objects.get_or_create(
<<<<<<< HEAD
<<<<<<< HEAD
                        name=row[0].lower(),
                        measurement_unit=row[1].lower()
                    )
=======
                        name=row[0],
                        measurement_unit=row[1]
                        )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                        name=row[0],
                        measurement_unit=row[1]
                        )
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        except Exception:
            raise CommandError('Ошибка заполнения базы данных')
