from django.db import models
import uuid
from django.utils import timezone


# Create your models here.
class Course(models.Model):
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4,
                          editable=False)
    name = models.CharField(null=False, max_length=100)
    start_date = models.DateField(null=True, default=timezone.now)
    count_of_students = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"
