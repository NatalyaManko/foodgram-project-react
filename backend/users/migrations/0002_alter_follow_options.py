# Generated by Django 4.2.10 on 2024-03-02 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ('-id',), 'verbose_name': 'подписка', 'verbose_name_plural': 'Подписки'},
        ),
    ]
