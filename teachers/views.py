from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from webargs.djangoparser import use_kwargs

from teachers.forms import TeacherCreateForm
from teachers.models import Teacher
from utils import format_records


@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "last_name": fields.Str(
            required=False,
        ),
        "faculty": fields.Str(
            required=False,
        ),
        "phone": fields.Str(
            required=False,
        ),
        "birthdate": fields.Date(
            required=False,
        ),
    },
    location="query",
)
def get_teachers(request, **params):
    teachers = Teacher.objects.all()
    for param_name, param_value in params.items():
        teachers = teachers.filter(**{param_name: param_value})
    result = format_records(teachers)

    return HttpResponse(result)


@csrf_exempt
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers-list'))

    elif request.method == 'GET':
        form = TeacherCreateForm()

    form_html = f"""
        <form method="POST">
          {form.as_p()}
          <input type="submit" value="Create">
        </form>
        """

    return HttpResponse(form_html)
