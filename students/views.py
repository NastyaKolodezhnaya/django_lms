from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import faker
from students.models import Student
from utils import format_records

from django.views.decorators.csrf import csrf_exempt
from students.forms import StudentCreateForm


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
    form = """
        <form >
          <label>First name:</label><br>
          <input type="text" name="first_name"><br>

          <label>Text:</label><br>
          <input type="text" name="text" placeholder="Enter text to search"><br><br>

          <input type="submit" value="Search">
        </form>
        """

    students = Student.objects.all().order_by('-id')
    text_fields = ['first_name', 'last_name', 'email']

    for param_key, param_value in params.items():
        if param_value:
            if param_key == 'text':
                or_filter = Q()
                for field in text_fields:
                    or_filter |= Q(**{f'{field}__contains': param_value})
                students = students.filter(or_filter)
            else:
                students = students.filter(**{param_key: param_value})

    result = format_records(students)
    response = form + result

    return HttpResponse(response)


@csrf_exempt
def create_students(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/students')

    elif request.method == "GET":
        form = StudentCreateForm()

    form_html = f"""
    <form method="POST">
        {form.as_p()}
        <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)
