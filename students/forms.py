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
    #
    # def clean(self):
    #     pass
