from django.forms import ModelForm, EmailField
from django.core.validators import ValidationError

from students.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationStudentForm(UserCreationForm):
    email = EmailField(max_length=200,
                       help_text="Registration without email is not possible!")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
