# Generated by Django 3.2.3 on 2024-03-01 01:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message='Цвет должен быть задан кодом (например: #E26C2D)', regex='^#[a-fA-F0-9]{1,6}$')], verbose_name='Цвет'),
        ),
    ]
