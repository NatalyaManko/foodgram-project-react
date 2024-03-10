from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active',)
    list_editable = ('is_active',)
    search_fields = ('last_name',)
   # list_display_links = None


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
