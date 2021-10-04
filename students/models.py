import datetime
from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=80, null=False)
    last_name = models.CharField(max_length=80, null=False)
    email = models.EmailField(max_length=120, null=True)
    birthdate = models.DateField(null=True, default=datetime.date.today())

    def __str__(self):
        return f'{self.full_name()}, {self.id}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        return datetime.datetime.year - self.birthdate.year
