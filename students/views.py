import fields as fields
from django.shortcuts import render
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


<<<<<<< Updated upstream
def hello(request):
    return HttpResponse("HELLO")


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
    )},
    location="query"
)
def get_students(request, params):
    students = Student.objects.all()

    for param_key, param_value in params.items():
        students = students.filter(**{param_key: param_value})

    result = format_records(students)
    return HttpResponse(result)