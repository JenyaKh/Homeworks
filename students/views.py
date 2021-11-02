from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy

from courses.models import Course
from students.forms import StudentCreateForm, StudentUpdateForm, RegistrationStudentForm
from students.models import Student
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = reverse_lazy('students:login')


class GenerateStudents(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_table.html'
    login_url = reverse_lazy('students:login')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Student.generate_instances(10)


class StudentList(LoginRequiredMixin, ListView):
    template_name = 'students/student_table.html'
    model = Student
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')


class StudentSearchList(LoginRequiredMixin, ListView):
    template_name = 'students/student_table.html'
    model = Student
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id')
        if not selected_id:
            selected_id = self.request.session['selected_id']
        if not selected_id or selected_id == "all":
            object_list = Student.objects.all().order_by('-id')
            self.extra_context['selected_id'] = ''
            self.request.session['selected_id'] = ''
        else:
            self.extra_context['selected_id'] = selected_id
            self.extra_context['selected_name'] = Course.objects.get(id=selected_id).name
            object_list = Student.objects.filter(course=selected_id)
            self.request.session['selected_id'] = selected_id

        search_text = self.request.GET.get('text')
        if search_text:
            object_list = object_list.filter(Q(first_name__contains=search_text) | Q(last_name__contains=search_text))

        return object_list


class StudentCreate(LoginRequiredMixin, CreateView):
    form_class = StudentCreateForm
    template_name = 'students/student_create.html'
    success_url = reverse_lazy('students:list')
    login_url = reverse_lazy('students:login')


class StudentUpdate(LoginRequiredMixin, UpdateView):
    form_class = StudentUpdateForm
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_update.html'
    login_url = reverse_lazy('students:login')

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'avatar': obj.avatar}
        return obj


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy('students:list')
    template_name = 'students/student_delete.html'
    login_url = reverse_lazy('students:login')

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'name': obj.full_name()}
        return obj


class PageNotFound(TemplateView):
    template_name = 'errors/404.html'


class RegistrationStudent(CreateView):
    form_class = RegistrationStudentForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        return super().form_valid(form)


class UserLogin(LoginView):
    pass


class LogoutStudent(LogoutView):
    template_name = 'registration/logged_out.html'


def send_email(request):
    email = EmailMessage(subject='Registration from LMS',
                         body="Test text",
                         to=['ekhapchenko@gmail.com'])
    email.send()
    return HttpResponse('Done')
