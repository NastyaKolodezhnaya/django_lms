from django.http import HttpResponse
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

from teachers.models import Teacher
from utils import format_records


# Create your views here.
@use_args({
    "first_name": fields.Str(
        required=False
    ),
    "last_name": fields.Str(
        required=False
    ),
    "age": fields.Int(
        required=False
    ),
    "email": fields.Email(
        required=False
    ),
    "specialization": fields.Str(
        required=False
    )},
    location="query"
)
def get_teachers(request, params):
    teachers = Teacher.objects.all()

    for param_name, param_value in params.items():
        teachers = teachers.filter(**{param_name: param_value})

    result = format_records(teachers)
    return HttpResponse(result)
