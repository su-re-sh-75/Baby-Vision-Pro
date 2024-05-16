from django.db import models

priorities = (
    ('High', 'High'),
    ('Medium', 'Medium'),
    ('Low', 'Low'),
    )
class Notification(models.Model):
    notification_text = models.CharField(max_length=300)
    priority_level = models.CharField(max_length=10, choices=priorities)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notification_text