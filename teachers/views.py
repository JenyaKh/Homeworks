from django.http import HttpResponse
from webargs import fields
from webargs.djangoparser import use_kwargs

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
