from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    def add_to_group(self, request, queryset):
        group_id = request.POST.get('group_id')
        group = Group.objects.get(pk=group_id)
        queryset.update(groups=group)

    add_to_group.short_description = 'Добавить в группу'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets += (('Groups', {'fields': ('groups',)}),)


CustomUserAdmin.list_filter = ('username', 'email',)
CustomUserAdmin.list_display += ('id',
                                 'username',
                                 'email',
                                 'first_name',
                                 'last_name',
                                 'password',
                                 'is_staff',
                                 'is_active',
                                 'is_superuser')
CustomUserAdmin.list_editable += ('username',
                                  'email',
                                  'first_name',
                                  'last_name',
                                  'password',
                                  'is_staff',
                                  'is_active',)
CustomUserAdmin.list_display_links = ('id',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
