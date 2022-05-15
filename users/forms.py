from django.forms import EmailField

from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegistrationUserForm(UserCreationForm):
    email = EmailField(max_length=200,
                       help_text="Registration without email is not possible!")

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
