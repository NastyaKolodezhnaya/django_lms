from django.forms import ModelForm
from django.core.validators import ValidationError

from students.models import Student


class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email']

    @staticmethod
    def normalize_name(name):
        return name.lower().strip().capitalize()

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        return self.normalize_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']

        return self.normalize_name(last_name)

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        if first_name == last_name:
            raise ValidationError('First and last names can\'t be equal')

    def clean_date(self):
        cleaned_data = super().clean()

        enroll_date = cleaned_data['enroll_date']
        graduate_date = cleaned_data['graduate_date']

        if enroll_date >= graduate_date:
            raise ValidationError('Graduate date must be after enroll date')
