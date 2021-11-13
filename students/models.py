from faker import Faker
import datetime

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete, post_init, post_migrate, pre_delete
from django.dispatch import receiver

from django.core.validators import MinLengthValidator, RegexValidator
from students.validators import no_elon_validator, prohibited_domains, older_than_18


class UserProfile(models.Model):
    ROLES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor')
    )

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    type = models.CharField(max_length=60, choices=ROLES)

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )
    birthdate = models.DateField(null=True, blank=True, default=datetime.date.today, validators=[older_than_18])

    avatar = models.ImageField(upload_to='avatar', null=True,
                               blank=True)
    resume = models.FileField(upload_to='resume', null=True,
                              blank=True)

    course = models.ForeignKey(
        "courses.Course", null=True, blank=True, related_name="user_course", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


class Person(models.Model):
    first_name = models.CharField(
        max_length=60, null=False, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=80, null=False, validators=[MinLengthValidator(2)]
    )
    email = models.EmailField(max_length=120, null=True,
                              blank=True, validators=[no_elon_validator, prohibited_domains])

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator("\d{10,14}")]
    )

    class Meta:
        abstract = True  # no Person table to create


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
