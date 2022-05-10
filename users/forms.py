from django.forms import ModelForm, EmailField
from django.core.validators import ValidationError

from users.models import UserProfile, CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationUserForm(UserCreationForm):
    email = EmailField(max_length=200,
                       help_text="Registration without email is not possible!")

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
