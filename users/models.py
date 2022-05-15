from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import datetime

import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from users.managers import CustomManager

from django.core.validators import RegexValidator


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), null=False, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated '
                    'as active. Unselect this instead of deleting '
                    'accounts.')
    )

    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=_('Designates whether this user can log into '
                    'the admin site.')
    )

    objects = CustomManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    user = models.OneToOneField(get_user_model(),
                                on_delete=models.CASCADE)

    phone_number = models.CharField(
        null=True, max_length=14, unique=True,
        blank=True, validators=[RegexValidator(r'+\d{12}')]
    )
    birthdate = models.DateField(null=True, blank=True,
                                 default=datetime.date.today)

    avatar = models.ImageField(upload_to='avatar', null=True,
                               blank=True)
    resume = models.FileField(upload_to='resume', null=True,
                              blank=True)

    course = models.ForeignKey(
        "courses.Course", null=True, blank=True, related_name="user_course",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"
