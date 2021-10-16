import datetime
from faker import Faker

from django.db import models
from django.core.validators import MinLengthValidator

from students.validators import no_elon_validator, prohibited_domains, older_than_18


class Student(models.Model):
    first_name = models.CharField(max_length=60, null=False, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=80, null=False, validators=[MinLengthValidator(2)])
    email = models.EmailField(max_length=120, null=True, unique=True, validators=[no_elon_validator, prohibited_domains])
    phone_number = models.CharField(null=True, max_length=14, unique=True)
    birthdate = models.DateField(null=True, default=datetime.date.today(), validators=[older_than_18])
    enroll_date = models.DateField(null=True)
    graduate_date = models.DateField(null=True)  # or validators[4_months_after_enrollment] as an option

    def __str__(self):
        return f'{self.full_name()}, {self.email} id({self.id})'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def age(self):
        return datetime.datetime.year - self.birthdate.year

    @classmethod
    def generate_instances(cls, count=10):
        faker = Faker()
        for _ in range(count):
            instance = Student(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                birthdate=faker.date_between(start_date='-30y', end_date='-18y'))
            instance.save()
