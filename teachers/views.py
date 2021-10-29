from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from courses.models import Course
from teachers.forms import TeacherCreateForm
from teachers.models import Teacher


class TeacherCreate(CreateView):
    form_class = TeacherCreateForm
    template_name = 'teachers/teacher_create.html'
    success_url = reverse_lazy('teachers:list')


class TeacherList(ListView):
    template_name = 'teachers/teacher_table.html'
    model = Teacher
    extra_context = {'courses': Course.objects.all()}


class TeacherSearchList(ListView):

    template_name = 'teachers/teacher_table.html'
    model = Teacher
    selected_id = None
    selected_name = None
    extra_context = {'courses': Course.objects.all(),
                     'selected_id': selected_id,
                     'selected_name': selected_name}

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id')
        if not selected_id:
            object_list = Teacher.objects.all().order_by('-id')
        else:
            self.selected_id = selected_id
            self.selected_name = Course.objects.get(id=selected_id).name
            object_list = Teacher.objects.filter(course=selected_id)

        return object_list
