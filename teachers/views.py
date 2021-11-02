from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from courses.models import Course
from teachers.forms import TeacherCreateForm
from teachers.models import Teacher


class TeacherCreate(LoginRequiredMixin, CreateView):
    form_class = TeacherCreateForm
    template_name = 'teachers/teacher_create.html'
    success_url = reverse_lazy('teachers:list')
    login_url = reverse_lazy('students:login')


class TeacherList(LoginRequiredMixin, ListView):
    template_name = 'teachers/teacher_table.html'
    model = Teacher
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')


class TeacherSearchList(LoginRequiredMixin, ListView):

    template_name = 'teachers/teacher_table.html'
    model = Teacher
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()

        return context

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id')
        if not selected_id:
            object_list = Teacher.objects.all().order_by('-id')
            self.extra_context['selected_id'] = ''
        else:
            self.extra_context['selected_id'] = selected_id
            self.extra_context['selected_name'] = Course.objects.get(id=selected_id).name
            object_list = Teacher.objects.filter(course=selected_id)

        return object_list
