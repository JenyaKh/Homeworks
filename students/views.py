from django.db.models import Q
from django.http import HttpResponse
from faker import Faker
from webargs import fields
from webargs.djangoparser import use_kwargs
from students.models import Student
from utils import format_records


def hello(request):
    return HttpResponse('SUCCESS')


def generate_students(request, count=10):
    faker = Faker()
    for i in range(count):
        st = Student(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            birthdate=faker.date_time_between(start_date="-30y", end_date="-18y")
        )
        st.save()
    return HttpResponse('SUCCESS')


@use_kwargs(
    {
        "first_name": fields.Str(
            required=False,
        ),
        "last_name": fields.Str(
            required=False,
        ),
        "email": fields.Str(
            required=False,
        ),
        "birthdate": fields.Date(
            required=False,
        ),
        "text": fields.Str(
            required=False,
        ),
    },
    location="query",
)
def get_students(request, **params):

    students = Student.objects.all()

    for param_name, param_value in params.items():
        if param_name == 'text':
            q_list = Q()
            q_list |= Q(first_name__icontains=param_value)
            q_list |= Q(last_name__icontains=param_value)
            q_list |= Q(email__icontains=param_value)

            students = students.filter(q_list)

        else:
            students = students.filter(**{param_name: param_value})

    result = format_records(students)

    return HttpResponse(result)
