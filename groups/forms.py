from django.forms import ModelForm
from django.core.validators import ValidationError

from groups.models import Group


class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['course', 'student_num']

    @staticmethod
    def normalize_name(course):
        return course.lower().strip().capitalize()

    def clean_email(self):
        email = self.cleaned_data['email']
        return self.normalize_name(email)
