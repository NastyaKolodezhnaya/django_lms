from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webargs.djangoparser import use_args, use_kwargs, DjangoParser
from django.core.exceptions import BadRequest
from webargs import fields
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

import students
from students.forms import StudentCreateForm
from students.models import Student
from utils import format_records


parser = DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def start(request):
    return HttpResponse('SUCCESS')


@use_args({
    # "first_name": fields.Str(
    #     required=False
    # ),
    # "last_name": fields.Str(
    #     required=False
    # ),
    "text": fields.Str(
        required=False
    )},
    location="query"
)
def get_students(request, params):

    form = """
        <form >
          <label>Text:</label><br>
          <input type="text" name="text" placeholder="Enter text to search"><br><br>

          <input type="submit" value="Search">
        </form>
        """

    students_rec = Student.objects.all().order_by('-id')

    text_fields = ['first_name', 'last_name', 'email']

    for param_key, param_value in params.items():
        if param_value:
            if param_key == 'text':
                or_filter = Q()
                for field in text_fields:
                    # or_filter = Q() | Q(**{f'{field}__contains': param_value})
                    or_filter |= Q(**{f'{field}__contains': param_value})
                students_rec = students_rec.filter(or_filter)
            else:
                students_rec = students_rec.filter(**params)

    result = format_records(students_rec, 'students')  # {students} - django app name to specify redirection

    response = form + result

    return HttpResponse(response)


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    # elif request.method == 'GET':
    form = StudentCreateForm()

    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Create">
    </form>
    """

    return HttpResponse(form_html)


@csrf_exempt
def update_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    form = StudentCreateForm(instance=student)
    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """
    return HttpResponse(form_html)
