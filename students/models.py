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
        "courses.Course", null=True, blank=True, related_name="student_course", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
