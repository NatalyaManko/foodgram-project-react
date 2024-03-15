from django.contrib.auth.admin import UserAdmin

UserAdmin.list_filter += ('username', 'email',)


class UserAdmin(UserAdmin):

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
                     'is_staff',
                     'is_active',)
    search_fields = ('last_name',)
    list_display_links = None
