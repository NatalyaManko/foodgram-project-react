from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

UserAdmin.list_filter = ('username', 'email',)
UserAdmin.list_display += ('id',
                           'username',
                           'email',
                           'first_name',
                           'last_name',
                           'password',
                           'is_staff',
                           'is_active',
                           'is_superuser')
UserAdmin.list_editable += ('username',
                            'email',
                            'first_name',
                            'last_name',
                            'password',
                            'is_staff',
                            'is_active',)
UserAdmin.list_display_links = ('id',)


admin.site.register(Group)
