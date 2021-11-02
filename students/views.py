from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage, send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return reverse("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html",
                  context={"password_reset_form": password_reset_form})
