import random

from django.db import models
from faker import Faker


# Create your models here.
class Teacher(models.Model):
    SPECIALIZATIONS = ['UI/UX Design', "QA Automation", 'Python Basic', 'Python Advanced', 'SMM', 'Java Essentials',
                       'FrontEnd Development', 'Machine Learning']

    first_name = models.CharField(max_length=60, null=False, default='not stated')
    last_name = models.CharField(max_length=60, null=False, default='not stated')
    age = models.IntegerField(null=True)
    email = models.EmailField(max_length=120, null=True)
    specialization = models.CharField(max_length=100, null=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name()}, id({self.id})'

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        for _ in range(count):
            instance = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                age=random.randrange(23, 80),
                email=faker.email(),
                specialization=random.choice(cls.SPECIALIZATIONS)
            )
            instance.save()
