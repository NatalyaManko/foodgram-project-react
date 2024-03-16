from django.contrib import admin
from django.db import models
from django.forms import widgets

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug', 'color',)
    list_editable = ('name', 'slug', 'color',)
    formfield_overrides = {
        models.CharField: {'widget': widgets.TextInput(
            attrs={'type': 'color'})
        },
    }
