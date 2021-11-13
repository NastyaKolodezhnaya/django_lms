from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import get_object_or_404
from webargs.djangoparser import use_args, DjangoParser
from django.core.exceptions import BadRequest
from django.forms.utils import ErrorList
from webargs import fields
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from django.shortcuts import render
from django.template import RequestContext

from students.forms import RegistrationStudentForm
from students.services.email_functions import send_registration_email
from students.models import UserProfile
from courses.models import Course
from django.contrib.auth.models import User

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import EmailMessage
from students.services.token_generator import TokenGenerator
from django.contrib.auth import login


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


class StudentSignIn(TemplateView):
    template_name = 'registration/sign_in.html'


class LoginStudent(LoginView):
    success_url = reverse_lazy('start')


class LogoutStudent(LogoutView):
    template_name = 'index.html'


class RegistrationStudent(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationStudentForm
    # create an html template saying 'Thanks for registration! We've sent you a confirmation letter, check it out!'
    success_url = reverse_lazy('start')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(request=self.request,
                                user_instance=self.object)
        return super().form_valid(form)


class ActivateUser(RedirectView):
    url = reverse_lazy('start')

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            user_pk = force_bytes(urlsafe_base64_decode(uidb64))
            current_user = get_user_model().objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError, TypeError):
            # create an html template saying 'Seems, you entered an invalid data! There is no such page, sorry!'
            return HttpResponse("Invalid data")

        if current_user:
            # if TokenGenerator().check_token(current_user, token): - token is not valid :\
            current_user.is_active = True
            current_user.save()

            login(request, current_user)
            return super().get(request, *args, **kwargs)

        return HttpResponse("Invalid data")


class GetStudents(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = UserProfile
    template_name = 'show.html'
    # extra_context = {'students_list': students,
    #                  'courses_list': Course.objects.all()}

    def get_context_data(self, **kwargs):
        # method must return a dict like 'extra_context' was
        course_id = self.kwargs.get('course')
        students = self.model.objects.all()
        courses = Course.objects.all()

        if course_id:
            students = students.filter(course__id__contains=course_id)
        return {
            'students_list': students,
            'courses_list': courses
        }


def search_students(request):
    search_text = request.GET.get('search')
    text_fields = ["first_name", "last_name", "email", 'course__name']
    students = self.model.objects.filter(type='student')

    if search_text:
        or_filter = Q()
        for field in text_fields:
            or_filter |= Q(**{f"{field}__icontains": search_text})
        students = students.filter(or_filter)

    return render(
        request=request,
        template_name="show.html",
        context={"students_list": students},
    )


class DeleteStudent(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = UserProfile
    success_url = reverse_lazy('students:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
