from colorfield.fields import ColorField
from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField('Название',
                            max_length=settings.CHAR_FIELD_MAX_LEN,
                            unique=True)
    color = ColorField('Цветовой код',
                       max_length=settings.HEX_FIELD_MAX_LEN,
                       unique=True,
                       null=False)
    slug = models.SlugField('Слаг',
                            max_length=settings.CHAR_FIELD_MAX_LEN,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Таг'
        verbose_name_plural = 'Таги'

    def __str__(self):
        return self.name
