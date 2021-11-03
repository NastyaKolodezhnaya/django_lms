from students.models import Person

from django.db import models
import uuid


# Create your models here.
class Teacher(Person):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ManyToManyField(to="students.Course", related_name="teacher_course")

    def __str__(self):
        return f"{self.first_name} {self.last_name}, ({self.id})"
