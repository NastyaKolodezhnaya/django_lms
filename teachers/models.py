from django.db import models

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    age = models.IntegerField(null=True)
    courses_headed = models.CharField(max_length=100, null=True)
    comments = models.CharField(max_length=100, null=True)
