from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webargs.djangoparser import use_args, DjangoParser
from django.core.exceptions import BadRequest
from django.forms.utils import ErrorList
from webargs import fields
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy

from django.shortcuts import render
from django.template import RequestContext

from students.forms import StudentCreateForm
from students.models import Student, Course

from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

parser = DjangoParser()


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise BadRequest(error.messages)


def handle_error_404(request, exception):
    context = RequestContext(request)
    response = render('404.html', context)
    response.status_code = 404
    return response


class IndexPage(TemplateView):
    template_name = 'index.html'


# need to refresh the page over & over again to reload info from db ??fix ++ course search through students records
class GetStudents(TemplateView):
    students = Student.objects.all()
    template_name = 'show.html'
    extra_context = {'students_list': Student.objects.all(),
                     'courses_list': Course.objects.all()}

    def course_filter(self):
        course = self.kwargs['course']  # trigger to the method, or how to filter records!!
        if course:
            self.students = self.students.filter(course__id__contains=course)
        return self.students

# @use_args({
#     "course": fields.Str(
#         required=False
#     )},
#     location="query"
# )
# def get_students(request, params):
#     students_rec = Student.objects.all()
#     courses_rec = Course.objects.all()
#
#     if params:
#         students_rec = students_rec.filter(course__id__contains=params['course'])
#
#     return render(
#         request=request,
#         template_name='show_students.html',
#         context={'students_list': students_rec,
#                  'courses_list': courses_rec}
#     )


def search_students(request):
    search_text = request.GET.get('search')
    text_fields = ["first_name", "last_name", "email", 'course__name']

    if search_text:
        or_filter = Q()
        for field in text_fields:
            or_filter |= Q(**{f"{field}__icontains": search_text})
        students_rec = Student.objects.filter(or_filter)
    else:
        students_rec = Student.objects.all()

    return render(
        request=request,
        template_name="show.html",
        context={"students_list": students_rec},
    )
# search_teacher view !!


class CreateStudent(CreateView):
    template_name = 'create.html'
    fields = "__all__"
    model = Student
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: add validation to the model 'validator' list!!
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class UpdateStudent(UpdateView):
    template_name = 'edit.html'
    fields = "__all__"
    model = Student
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # TODO: add validation to the model 'validator' list!!
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class DeleteStudent(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
