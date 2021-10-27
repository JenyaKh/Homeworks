from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from courses.models import Course
from students.forms import StudentCreateForm, StudentUpdateForm
from students.models import Student
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView


def hello(request):
    return HttpResponse('SUCCESS')


class IndexView(TemplateView):
    template_name = 'index.html'


def generate_students(request, count=10):
    Student.generate_instances(count)
    return HttpResponse('SUCCESS')


class StudentList(ListView):
    template_name = 'students/student_table.html'
    model = Student

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super(StudentList, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['selected_id'] = "all"
        context['selected_name'] = "All courses"
        self.request.session['selected_id'] = "all"
        self.request.session['selected_name'] = 'All courses'

        return context


class StudentSearchList(ListView):

    template_name = 'students/student_table.html'
    model = Student

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudentSearchList, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['selected_id'] = self.request.session['selected_id']
        context['selected_name'] = self.request.session['selected_name']

        return context

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id', None)

        if not selected_id:
            selected_id = self.request.session['selected_id']
        if selected_id == "all":
            self.request.session['selected_name'] = "All courses"
            self.request.session['selected_id'] = "all"
            object_list = Student.objects.all().order_by('-id')
        else:
            self.request.session['selected_name'] = Course.objects.get(id=selected_id).name
            self.request.session['selected_id'] = selected_id
            object_list = Student.objects.filter(course=selected_id)

        search_text = self.request.GET.get('text', None)
        if search_text:
            object_list = object_list.filter(Q(first_name__contains=search_text) | Q(last_name__contains=search_text))

        return object_list


class StudentCreate(CreateView):
    form_class = StudentCreateForm
    template_name = 'students/student_create.html'
    success_url = reverse_lazy('students:list')


class StudentUpdate(UpdateView):
    form_class = StudentUpdateForm
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_update.html'

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data()
        context['avatar'] = self.object.avatar
        return context


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_delete.html'

    def get_context_data(self, **kwargs):
        context = super(StudentDelete, self).get_context_data()
        context['name'] = self.object.full_name()
        return context


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)
