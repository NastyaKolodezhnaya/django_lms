from django.forms import ModelForm
from django.core.validators import ValidationError

from teachers.models import Teacher


class TeacherCreateForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'specialization']

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
