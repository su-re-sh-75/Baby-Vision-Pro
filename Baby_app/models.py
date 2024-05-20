from django.db import models

priorities = (("High", "High"),
              ("Medium", "Medium"),
              ("Low", "Low"))

    
class Notification(models.Model):
    notification_text = models.CharField(max_length=200)
    received_at = models.DateTimeField(auto_now_add=True)
    priority_level = models.CharField(choices=priorities, max_length=20)
        
    class Meta:
        app_label = 'Baby_app'

    def __str__(self) -> str:
        return self.notification_text