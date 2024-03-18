from django.contrib.auth.admin import UserAdmin

UserAdmin.list_display = ('username',
                          'email')
UserAdmin.search_fields += ('username', 'email')
