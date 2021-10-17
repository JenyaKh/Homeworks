from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from webargs.djangoparser import use_kwargs

from students.forms import StudentCreateForm, StudentUpdateForm
from students.models import Student


def hello(request):
    return HttpResponse('SUCCESS')


def index(request):
    return render(
        request=request,
        template_name="index.html",
    )


def generate_students(request, count=10):
    Student.generate_instances(count)
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

    students = Student.objects.all().order_by('-id')

    for param_name, param_value in params.items():
        if param_name == 'text':
            q_list = Q()
            q_list |= Q(first_name__icontains=param_value)
            q_list |= Q(last_name__icontains=param_value)
            q_list |= Q(email__icontains=param_value)

            students = students.filter(q_list)

        else:
            students = students.filter(**{param_name: param_value})

    return render(
        request=request,
        template_name="students/students_table.html",
        context={"students_list": students}
    )


def search_student(request):
    query = request.GET.get('text')
    object_list = Student.objects.filter(
        Q(first_name__startswith=query) | Q(last_name__startswith=query)
    )
    return render(
        request=request,
        template_name="students/students_table.html",
        context={"students_list": object_list}
    )


@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentCreateForm()

    return render(
        request=request,
        template_name="students/students_create.html",
        context={"form": form}
    )


@csrf_exempt
def update_student(request, pk):

    student = get_object_or_404(Student, id=pk)

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentUpdateForm(instance=student)

    return render(
        request=request,
        template_name="students/students_update.html",
        context={"form": form}
    )


def delete_student(request, pk):

    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse('students:list'))


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)
