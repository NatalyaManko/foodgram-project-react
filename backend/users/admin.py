from django.contrib import admin

from .models import Follow, User


class UserAdmin(admin.ModelAdmin):

    list_display = ('id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'password',
                    'is_staff',
                    'is_active',
                    'is_superuser')
    list_editable = ('username',
                     'email',
                     'first_name',
                     'last_name',
                     'password',
                     'is_active',)
    search_fields = ('last_name',)
    list_display_links = None


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
