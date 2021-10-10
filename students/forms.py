from django.forms import ModelForm
from django.core.validators import ValidationError
from students.models import Student


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']

        if email.endswith('@mail.ru') or email.endswith('@yandex.ru'):
            raise ValidationError('Such domain is not accepted. Please, use another email')

        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.lower().strip().capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.lower().strip().capitalize()
