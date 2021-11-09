from django.forms import ModelForm
# from django.core.validators import ValidationError
from teachers.models import Teacher


class TeacherCreateForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "email", "phone_number", "course"]
