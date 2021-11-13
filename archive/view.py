# from django.urls import reverse, reverse_lazy
# from django.shortcuts import get_object_or_404
# from webargs import fields
# from django.urls import reverse, reverse_lazy
# from django.template import RequestContext
#
# from students.forms import RegistrationStudentForm
# from students.models import UserProfile
# from courses.models import Course
# from django.contrib.auth.models import User
#
# from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, RedirectView


# class CreateStudent(LoginRequiredMixin, CreateView):
#     login_url = reverse_lazy('sign_in')
#     template_name = 'create.html'
#     fields = "__all__"
#     model = UserProfile
#     success_url = reverse_lazy('students:list')
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         # TODO: add validation to the model 'validator' list!!
#         first_name = form.cleaned_data["first_name"]
#         last_name = form.cleaned_data["last_name"]
#         if first_name == last_name:
#             form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
#             form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
#             return super().form_invalid(form)
#         return super().form_valid(form)
#
#
# class UpdateStudent(LoginRequiredMixin, UpdateView):
#     login_url = reverse_lazy('sign_in')
#     template_name = 'edit.html'
#     fields = "__all__"
#     model = UserProfile
#     success_url = reverse_lazy('students:list')
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         # TODO: add validation to the model 'validator' list!!
#         first_name = form.cleaned_data["first_name"]
#         last_name = form.cleaned_data["last_name"]
#         if first_name == last_name:
#             form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
#             form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
#             return super().form_invalid(form)
#         return super().form_valid(form)
