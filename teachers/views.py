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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['selected_id'] = "all"
        context['selected_name'] = "All courses"

        return context


class TeacherSearchList(ListView):

    template_name = 'teachers/teacher_table.html'
    model = Teacher
    extra_context = {'courses': Course.objects.all()}

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()

        return context

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id', 'all')
        if selected_id == "all":
            self.extra_context = {'selected_id': "all", 'selected_name': "All courses"}
            object_list = Teacher.objects.all().order_by('-id')
        else:
            self.extra_context = {'selected_id': selected_id,
                                  'selected_name': Course.objects.get(id=selected_id).name}
            object_list = Teacher.objects.filter(course=selected_id)

        return object_list
