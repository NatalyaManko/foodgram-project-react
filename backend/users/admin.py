from django.contrib.auth.admin import UserAdmin

UserAdmin.list_filter += ('username', 'email',)
