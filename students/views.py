from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from webargs import fields
from webargs.djangoparser import use_kwargs

from students.forms import StudentCreateForm, StudentUpdateForm, TeacherCreateForm
from students.models import Student, Teacher, Course


def hello(request):
    return HttpResponse('SUCCESS')


def clean_session(request):
    request.session['students_course'] = []
    request.session['students_search'] = []


def students_session(request, first_filter, second_filter, objects_list):
    request.session[first_filter] = []
    list_students = request.session[second_filter]
    if list_students:
        or_filter = Q()
        for student_id in list_students:
            or_filter |= Q(id=student_id)
        objects_list = objects_list.filter(or_filter)
    for obj in objects_list:
        request.session[first_filter].append(obj.id)
    request.session.modified = True
    return objects_list


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
    clean_session(request)
    students = Student.objects.all().order_by('-id')
    courses = Course.objects.all()

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
        template_name="students/student_table.html",
        context={"objects_list": students,
                 "courses": courses,
                 "selected_id": "all",
                 "selected_name": "All courses"
                 }
    )


def search_student(request):
    courses = Course.objects.all()
    query = request.GET.get('text')
    if not query:
        return HttpResponseRedirect(reverse('students:list'))
    else:
        objects_list = Student.objects.filter(Q(first_name__contains=query) | Q(last_name__contains=query))
    objects_list = students_session(request, 'students_search', 'students_course', objects_list)
    return render(
        request=request,
        template_name="students/student_table.html",
        context={"objects_list": objects_list,
                 "courses": courses,
                 "selected_id": request.session['selected_id'],
                 "selected_name": request.session['selected_name'], }
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
        template_name="students/student_create.html",
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
        template_name="students/student_update.html",
        context={"form": form}
    )


def delete_student(request, pk):

    student = get_object_or_404(Student, id=pk)
    student.delete()

    return HttpResponseRedirect(reverse('students:list'))


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)


@csrf_exempt
def create_teacher(request):
    if request.method == "POST":
        form = TeacherCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("students:list-teachers"))

    elif request.method == "GET":
        form = TeacherCreateForm()

    return render(
        request=request,
        template_name="students/teacher_create.html",
        context={"form": form}
    )


def get_teachers(request):
    clean_session(request)
    courses = Course.objects.all()
    teachers = Teacher.objects.all().order_by('-id')

    return render(
        request=request,
        template_name="students/teacher_table.html",
        context={"objects_list": teachers,
                 "courses": courses,
                 "selected_id": "all",
                 "selected_name": "All courses"
                 }
    )


def search_by_course(request, model, template_name):
    selected_id = request.GET.get('course_id')
    courses = Course.objects.all()
    if selected_id == "all":
        objects_list = model.objects.all()
        selected_name = "All courses"
    else:
        objects_list = model.objects.filter(course=selected_id)
        selected_name = Course.objects.get(id=selected_id).name
    if model == Student:
        request.session['selected_id'] = selected_id
        request.session['selected_name'] = selected_name
        objects_list = students_session(request, 'students_course', 'students_search', objects_list)
    return render(
        request=request,
        template_name=template_name,
        context={"objects_list": objects_list,
                 "courses": courses,
                 "selected_id": selected_id,
                 "selected_name": selected_name, }
    )
