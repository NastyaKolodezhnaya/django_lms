from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from webargs.djangoparser import use_args, use_kwargs
from webargs import fields

import teachers
from teachers.models import Teacher
from students.models import Course

from django.shortcuts import render
from django.template import RequestContext
from teachers.forms import TeacherCreateForm


# Create your views here.
@use_args({
    "course": fields.Str(
        required=False
    )},
    location="query"
)
def get_teachers(request, params):
    teachers_rec = Teacher.objects.all()
    courses_rec = Course.objects.all()

    text_fields = ['first_name', 'last_name', 'email', 'course__name']

    if request.method == 'GET':
        search_text = request.GET.get('search_box', None)
        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f'{field}__contains': search_text})
            teachers_rec = teachers_rec.filter(or_filter)

    if params:
        teachers_rec = teachers_rec.filter(course__id__contains=params['course'])

    return render(
        request=request,
        template_name='show_teachers.html',
        context={'teachers_list': teachers_rec,
                 'courses_list': courses_rec}
    )


@csrf_exempt
def create_teacher(request):

    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list'))

    form = TeacherCreateForm()

    return render(
        request=request,
        template_name='create_teacher.html',
        context={'create_teacher': form}
    )
