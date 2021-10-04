from django.shortcuts import render
from django.http import HttpResponse

import faker


# Create your views here
def start(request):
    return HttpResponse('SUCCESS')


def hello(request):
    return HttpResponse("HELLO")


def generate_students(request, count=10):
    fake_student = faker.Faker('RU')
    students = [fake_student.name() for n in range(14)]
    result = '<br>'.join(students)
    return HttpResponse(result)
