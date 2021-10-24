from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from students.forms import StudentCreateForm, StudentUpdateForm, TeacherCreateForm
from students.models import Student, Teacher, Course


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


def get_students(request, selected_id=None):
    courses = Course.objects.all()
    if request.GET.get('course_id'):
        selected_id = request.GET.get('course_id')
    if not selected_id:
        selected_id = request.session['selected_id']
    if selected_id == "all":
        objects_list = Student.objects.all().order_by('-id')
        selected_name = "All courses"
    else:
        objects_list = Student.objects.filter(course=selected_id)
        selected_name = Course.objects.get(id=selected_id).name
    request.session['selected_id'] = selected_id
    request.session['selected_name'] = selected_name
    request.session.modified = True
    if request.GET.get('text'):
        query = request.GET.get('text')
        objects_list = objects_list.filter(Q(first_name__contains=query) | Q(last_name__contains=query))

    return render(
        request=request,
        template_name="students/student_table.html",
        context={"objects_list": objects_list,
                 "courses": courses,
                 "selected_id": selected_id,
                 "selected_name": selected_name
                 }
    )


@csrf_exempt
def create_student(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST, request.FILES)
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
        form = StudentUpdateForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('students:list'))

    elif request.method == 'GET':
        form = StudentUpdateForm(instance=student)

    img_path = Student.objects.get(id=pk).avatar

    return render(
        request=request,
        template_name="students/student_update.html",
        context={"form": form,
                 "img_path": img_path}

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


def get_teachers(request, selected_id=None):
    courses = Course.objects.all()
    if request.GET.get('course_id'):
        selected_id = request.GET.get('course_id')
    if not selected_id:
        selected_id = request.session['selected_id']
    if selected_id == "all":
        objects_list = Teacher.objects.all().order_by('-id')
        selected_name = "All courses"
    else:
        objects_list = Teacher.objects.filter(course=selected_id)
        selected_name = Course.objects.get(id=selected_id).name

    return render(
        request=request,
        template_name="students/teacher_table.html",
        context={"objects_list": objects_list,
                 "courses": courses,
                 "selected_id": selected_id,
                 "selected_name": selected_name
                 }
    )
