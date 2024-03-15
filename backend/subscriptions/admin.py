from django.contrib import admin

from subscriptions.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('author', 'user')


admin.site.register(Subscription, SubscriptionAdmin)
