from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from django.shortcuts import render
from webargs.djangoparser import DjangoParser
from django.core.exceptions import BadRequest
from django.template import RequestContext

from users.forms import RegistrationUserForm
from users.services.email_functions import send_registration_email
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.views.generic import TemplateView, CreateView, RedirectView
from django.contrib.auth.views import LoginView, LogoutView

from django.core.mail import EmailMessage
from users.services.token_generator import TokenGenerator
from django.contrib.auth import login


parser = DjangoParser()


# Create your views here.
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


class UserSignIn(TemplateView):
    template_name = 'registration/sign_in.html'


class LoginUser(LoginView):
    success_url = reverse_lazy('start')


class LogoutUser(LogoutView):
    template_name = 'index.html'


class RegistrationUser(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationUserForm
    success_url = reverse_lazy('sign_in')

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
        print(f'token: {token}')

        try:
            user_pk = force_bytes(urlsafe_base64_decode(uidb64))
            current_user = get_user_model().objects.get(pk=user_pk)
        except (User.DoesNotExist, ValueError, TypeError):
            # create an html template saying 'Seems, you entered an invalid data! There is no such page!'
            return HttpResponse("Invalid data")

        if current_user.is_active:
            return super().get(request, *args, **kwargs)

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user, backend='django.contrib.auth.backends.ModelBackend')
            return super().get(request, *args, **kwargs)

        return HttpResponse("Invalid data")
