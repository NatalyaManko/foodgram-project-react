from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from .models import Follow, User


@csrf_exempt
class UserAdmin(admin.ModelAdmin):

    list_display = ('__all__',)
    list_editable = ('__all__',)
    search_fields = ('last_name',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
