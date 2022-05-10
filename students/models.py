from faker import Faker
import datetime

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from django.core.validators import MinLengthValidator, RegexValidator
from students.validators import prohibited_domains, older_than_18


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True,
                              blank=True, validators=[prohibited_domains])

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )

    class Meta:
        abstract = True


class Student(Person):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    birthdate = models.DateField(null=True, blank=True, default=datetime.date.today, validators=[older_than_18])

    avatar = models.ImageField(upload_to='avatar', null=True,
                               blank=True)
    resume = models.FileField(upload_to='resume', null=True,
                              blank=True)

    course = models.ForeignKey(
        "courses.Course", null=True, blank=True, related_name="student_course", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.full_name()}, {self.age()}, {self.email} ({self.id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def age(self):
        if self.birthdate:
            return datetime.datetime.now().year - self.birthdate.year
        return 'Enter a valid birthdate, please!'

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            st = cls(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                phone_number=f'+380{faker.msisdn()[3:]}',
                birthdate=faker.date_time_between(start_date="-30y",
                                                  end_date="-18y")
            )
            st.save()
