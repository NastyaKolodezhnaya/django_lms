from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webargs.djangoparser import use_args, DjangoParser
from django.core.exceptions import BadRequest
from webargs import fields
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from students.forms import StudentCreateForm
from students.models import Student

from django.shortcuts import render
from django.template import RequestContext


parser = DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def handle_error_404(request, exception):
    context = RequestContext(request)
    response = render('404.html', context)
    response.status_code = 404
    return response


def index(request):
    return render(
        request=request,
        template_name='index.html',
        context={
            'param1': ' some output '
        }
    )


@use_args({
    "text": fields.Str(
        required=False
    )},
    location="query"
)
def get_students(request, params):
    students_rec = Student.objects.all()

    text_fields = ['first_name', 'last_name', 'email']

    # for param_key, param_value in params.items():
    #     if param_value:
    #         if param_key == 'text':
    #             or_filter = Q()
    #             for field in text_fields:
    #                 # or_filter = Q() | Q(**{f'{field}__contains': param_value})
    #                 or_filter |= Q(**{f'{field}__contains': param_value})
    #             students_rec = students_rec.filter(or_filter)
    #         else:
    #             students_rec = students_rec.filter(**params)

    if request.method == 'GET':
        search_text = request.GET.get('search_box', None)
        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f'{field}__contains': search_text})
            students_rec = students_rec.filter(or_filter)

    return render(
        request=request,
        template_name='show_students.html',
        context={'students_list': students_rec}
    )


@csrf_exempt
def create_student(request):

    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    form = StudentCreateForm()

    # form_html = f"""
    # <form method="POST">
    #   {form.as_p()}
    #   <input type="submit" value="Create">
    # </form>
    # """

    return render(
        request=request,
        template_name='create.html',
        context={'create_form': form}
    )


@csrf_exempt
def update_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        form = StudentCreateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list"))

    form = StudentCreateForm(instance=student)

    return render(
        request=request,
        template_name='edit.html',
        context={'edit_form': form}
    )


def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse("students:list"))
