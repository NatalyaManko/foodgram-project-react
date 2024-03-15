from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField('Название',
                            max_length=settings.CHAR_FIELD_MAX_LEN,
                            unique=True)
    color = models.CharField('Цвет',
                             max_length=settings.HEX_FIELD_MAX_LEN,
                             null=False,
                             validators=(RegexValidator(
                                 regex='^#[a-fA-F0-9]{1,6}$',
                                 message='Цвет должен быть задан кодом '
                                 + '(например: #E26C2D)'),))
    slug = models.SlugField('Слаг',
                            max_length=settings.CHAR_FIELD_MAX_LEN,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Таг'
        verbose_name_plural = 'Таги'

    def __str__(self):
        return self.name
