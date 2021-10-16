import datetime
from datetime import date
import random
from random import randrange

from faker import Faker
from django.db import models


# Create your models here.
class Group(models.Model):

    COURSES_AVAILABLE = ['UI/UX Design', "QA Automation", 'Python Basic', 'Python Advanced', 'SMM', 'Java Essentials',
                         'FrontEnd Development', 'Machine Learning']

    # group_name = models.CharField(max_length=80, null=False)
    course = models.CharField(max_length=40, null=False)
    student_num = models.IntegerField(null=False)
    start_date = models.DateField(null=True, default=date.today())

    def __str__(self):
        return f'{self.group_name()}, (id {self.id})'

    def group_name(self):
        return f"{self.course}('{self.start_date}')"

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        for _ in range(count):
            instance = cls(
                # group_name=instance.course + instance.start_date variable reference before assignment!!
                course=random.choice(cls.COURSES_AVAILABLE),
                student_num=randrange(5, 30),
                start_date=faker.date_between(start_date='-5y', end_date=datetime.date.today()))
            instance.save()
