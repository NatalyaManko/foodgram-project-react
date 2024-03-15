from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'slug', 'color',)
    list_editable = ('name', 'slug', 'color',)


admin.site.register(Tag, TagAdmin)
