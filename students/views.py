from django.http import HttpResponse
from django.db.models import Q
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import faker
from students.models import Student
from utils import format_records


# Create your views here

def start(request):
    return HttpResponse('SUCCESS')


def generate_students(request, count=10):
    fake_student = faker.Faker('RU')
    students = [fake_student.name() for n in range(14)]
    result = '<br>'.join(students)
    return HttpResponse(result)


@use_args({
    "first_name": fields.Str(
        required=False
    ),
    "last_name": fields.Str(
        required=False
    ),
    "text": fields.Str(
        required=False
    )},
    location="query"
)
def get_students(request, params):
    students = Student.objects.all()
    text_fields = ['first_name', 'last_name', 'email']

    for param_key, param_value in params.items():
        if param_key == 'text':
            students = students.filter(Q(members='me'))
        else:
            students = students.filter(**{param_key: param_value})

    result = format_records(students)
    return HttpResponse(result)