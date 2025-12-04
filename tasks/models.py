from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Baja', 'Baja'),
        ('Media', 'Media'),
        ('Alta', 'Alta'),
    ]

    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descripción")
    date = models.DateField(verbose_name="Fecha")
    time = models.TimeField(verbose_name="Hora")
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='Baja',
        verbose_name="Prioridad"
    )
    reminder_sent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.priority}"


class ReminderSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reminder_settings')
    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    reminder_time = models.IntegerField(default=15, help_text="Minutes before task")
    quiet_start = models.TimeField(default="22:00")
    quiet_end = models.TimeField(default="07:00")

    def __str__(self):
        return f"Settings for {self.user.username}"
