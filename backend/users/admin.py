from django.contrib.auth.admin import UserAdmin

UserAdmin.search_fields += ('username', 'email')
UserAdmin.list_display = ('username',
                          'email')
