from django.db.models import Q
from django.forms.utils import ErrorList
from webargs import fields
from django.urls import reverse, reverse_lazy
from django.shortcuts import render

from students.models import Student
from courses.models import Course

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login


class GetStudents(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users:sign_in')
    model = Student
    template_name = 'show.html'

    def get_context_data(self, **kwargs):
        course_id = self.request.GET.get('course')
        students = self.model.objects.all()
        courses = Course.objects.all()

        if course_id:
            students = students.filter(course__id__contains=course_id)
        return {
            'students_list': students,
            'courses_list': courses
        }


class SearchStudent(ListView):
    model = Student
    template_name = 'show.html'

    def get_context_data(self, **kwargs):
        search_text = self.request.GET.get('search')
        students = self.model.objects.all()
        text_fields = ["first_name", "last_name", "email", 'course__name']

        if search_text:
            or_filter = Q()
            for field in text_fields:
                or_filter |= Q(**{f"{field}__icontains": search_text})
            students = Student.objects.filter(or_filter)

        return {
            'students_list': students
        }


class CreateStudent(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('users:sign_in')
    template_name = 'create.html'
    fields = "__all__"
    model = Student
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class UpdateStudent(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('users:sign_in')
    template_name = 'edit.html'
    fields = "__all__"
    model = Student
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        if first_name == last_name:
            form._errors["first_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            form._errors["last_name"] = ErrorList(["First and last name cannot be equal, bro!"])
            return super().form_invalid(form)
        return super().form_valid(form)


class DeleteStudent(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('users:sign_in')
    model = Student
    success_url = reverse_lazy('students:list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
