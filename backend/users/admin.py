from django.contrib import admin

<<<<<<< HEAD
from .models import Follow, User


class UserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active',)
    list_editable = ('is_active',)
    search_fields = ('last_name',)
   # list_display_links = None


admin.site.register(User, UserAdmin)
admin.site.register(Follow)
=======
from .models import User, Follow

admin.site.register(User)
admin.site.register(Follow)
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
