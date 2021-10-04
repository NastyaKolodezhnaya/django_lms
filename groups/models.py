import datetime

from django.db import models

# Create your models here.
class Group(models.Model):
    group_name = models.CharField(max_length=80, null=False)
    st_number = models.IntegerField(null=False)
    start_date = models.DateTimeField(null=True, default=datetime.date.today())
    course = models.CharField(max_length=40, null=False)
