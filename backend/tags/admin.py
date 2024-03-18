from django.contrib import admin
from django.db import models
from django.forms import widgets

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('name', 'slug', 'color',)
    list_editable = ('color',)

    formfield_overrides = {
        models.CharField: {'widget': widgets.TextInput},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'color':
            kwargs['widget'] = widgets.TextInput(attrs={'type': 'color'})
        return super().formfield_for_dbfield(db_field, **kwargs)
