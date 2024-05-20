from django.contrib import admin


from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ["notification_text", "received_at", "priority_level"]
    list_filter = ["received_at", "priority_level"]

admin.site.register(Notification, NotificationAdmin)