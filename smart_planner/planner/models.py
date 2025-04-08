from django.db import models
from django.contrib.auth.models import User

class StudyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    reminder_time = models.IntegerField(null=True, blank=True) 

    def __str__(self):
        return self.subject


class StudyGoal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weekly_hours = models.IntegerField(default=5)
    target_tasks = models.IntegerField(default=10)
