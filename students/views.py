from django.http import HttpResponse
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import faker
from students.models import Student
from utils import format_records


# Create your views here

def start(request):
    return HttpResponse('SUCCESS')


def hello(request):
    return HttpResponse("HELLO")


@use_args({
    "first_name": fields.Str(
        required=False
    ),
    "last_name": fields.Str(
        required=False
    )},
    location="query"
)
def get_students(request, params):
    students = Student.objects.all()

    for param_key, param_value in params.items():
        students = students.filter(**{param_key: param_value})

    result = format_records(students)
    return HttpResponse(result)
