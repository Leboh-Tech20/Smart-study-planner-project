from django.db import models
from django.contrib.auth.models import User

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class StudyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject
