from django.db.models import Q
from django.urls import reverse_lazy

from courses.models import Course
from students.forms import StudentCreateForm, StudentUpdateForm
from students.models import Student
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView


class IndexView(TemplateView):
    template_name = 'index.html'


class GenerateStudents(ListView):
    model = Student
    template_name = 'students/student_table.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Student.generate_instances(10)


class StudentList(ListView):
    template_name = 'students/student_table.html'
    model = Student
    extra_context = {'courses': Course.objects.all()}


class StudentSearchList(ListView):
    template_name = 'students/student_table.html'
    model = Student
    selected_id = None
    selected_name = None
    extra_context = {'selected_id': selected_id,
                     'selected_name': selected_name,
                     'courses': Course.objects.all()}

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id')
        if not selected_id:
            selected_id = self.request.session['selected_id']
        if not selected_id:
            object_list = Student.objects.all().order_by('-id')
        else:
            self.selected_id = self.request.session['selected_id'] = selected_id
            self.selected_name = Course.objects.get(id=selected_id).name
            object_list = Student.objects.filter(course=selected_id)

        search_text = self.request.GET.get('text')
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

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'avatar': obj.avatar}
        return obj


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'name': obj.full_name()}
        return obj


class PageNotFound(TemplateView):
    template_name = 'errors/404.html'
