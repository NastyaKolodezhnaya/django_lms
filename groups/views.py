from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs.djangoparser import use_args
from webargs import fields
from groups.models import Group
from groups.forms import GroupCreateForm
from utils import format_records


@use_args({
    "course": fields.Str(
        required=False
    )},
    location="query"
)
def get_groups(request, params):

    groups = Group.objects.all().order_by('-id')

    if params:
        groups = groups.filter(**params)

    result = format_records(groups)
    return HttpResponse(result)


@csrf_exempt
def create_group(request):

    if request.method == "POST":
        form = GroupCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('groups:list'))

    form = GroupCreateForm()
    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)
