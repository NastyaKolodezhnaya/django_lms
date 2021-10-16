from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import teachers
from teachers.forms import TeacherCreateForm
from teachers.models import Teacher
from utils import format_records


# Create your views here.
@use_args({
    "text": fields.Str(
        required=False
    )},
    location="query"
)
def get_teachers(request, params):
    teachers_rec = Teacher.objects.all().order_by('-id')
    text_fields = ['first_name', 'last_name', 'specialization', 'email']

    form = """
        <form >
          <label>Text:</label><br>
          <input type="text" name="text" placeholder="Enter text to search"><br><br>

          <input type="submit" value="Search">
        </form>
        """

    for param_key, param_value in params.items():
        if param_value:
            if param_key == 'text':
                or_filter = Q()
                for field in text_fields:
                    # or_filter = Q() | Q(**{f'{field}__contains': param_value})
                    or_filter |= Q(**{f'{field}__contains': param_value})
                teachers_rec = teachers_rec.filter(or_filter)

    result = format_records(teachers_rec, 'teachers')
    return HttpResponse(form + result)


@csrf_exempt
def create_teacher(request):

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))

    # elif request.method == 'GET':
    form = TeacherCreateForm()
    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)


@csrf_exempt
def update_teacher(request, pk):

    teacher = get_object_or_404(Teacher, id=pk)

    if request.method == "POST":
        form = TeacherCreateForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("teachers:list"))

    form = TeacherCreateForm(instance=teacher)
    form_html = f"""
    <form method="POST">
      {form.as_p()}
      <input type="submit" value="Save">
    </form>
    """
    return HttpResponse(form_html)
