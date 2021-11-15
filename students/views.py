from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode

from courses.models import Course
from students.forms import StudentUpdateForm, RegistrationStudentForm
from students.models import Profile, CustomUser

from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, RedirectView

from students.services.emails import send_registration_email
from students.token_generator import TokenGenerator


class IndexView(TemplateView):
    template_name = 'index.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.request.session['type'] = None
        self.request.session['selected_id'] = None


class GenerateStudents(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'students/student_table.html'
    login_url = reverse_lazy('students:login')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Profile.generate_instances(10)


class StudentList(LoginRequiredMixin, ListView):
    template_name = 'students/student_table.html'
    model = Profile
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')
    pk_url_kwarg = 'type'

    def get_queryset(self):
        object_list = super().get_queryset()
        profile_type = None
        if self.kwargs.get('type', None):
            profile_type = self.kwargs['type']
        if not profile_type:
            profile_type = self.request.session.get('type')
        if profile_type:
            if profile_type != 'all':
                object_list = object_list.filter(type=profile_type)
                self.request.session['type'] = profile_type
            else:
                self.request.session['type'] = None
        return object_list


class StudentSearchList(LoginRequiredMixin, ListView):
    template_name = 'students/student_table.html'
    model = Profile
    extra_context = {'courses': Course.objects.all()}
    login_url = reverse_lazy('students:login')

    def get_queryset(self):

        selected_id = self.request.GET.get('course_id')
        if not selected_id:
            selected_id = self.request.session.get('selected_id', None)

        if not selected_id or selected_id == "all":
            object_list = Profile.objects.all().order_by('-id')
            self.extra_context['selected_id'] = ''
            self.request.session['selected_id'] = ''
        else:
            self.extra_context['selected_id'] = selected_id
            self.extra_context['selected_name'] = Course.objects.get(id=selected_id).name
            object_list = Profile.objects.filter(course=selected_id)
            self.request.session['selected_id'] = selected_id

        search_text = self.request.GET.get('text')
        if search_text:
            object_list = object_list.filter(Q(first_name__contains=search_text) | Q(last_name__contains=search_text))

        profile_type = self.request.session.get('type')
        print(profile_type)
        if profile_type:
            object_list = object_list.filter(type=profile_type)

        return object_list


class StudentUpdate(LoginRequiredMixin, UpdateView):
    form_class = StudentUpdateForm
    model = Profile
    template_name = 'students/student_update.html'
    login_url = reverse_lazy('students:login')
    success_url = reverse_lazy('students:list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'avatar': obj.avatar}

        return obj


class StudentProfile(UpdateView):
    form_class = StudentUpdateForm
    model = Profile
    template_name = 'students/student_update.html'
    success_url = reverse_lazy('students:list')

    def get_object(self, queryset=None):
        user = CustomUser.objects.get(pk=self.kwargs['pk'])
        profiles = Profile.objects.filter(user_id=user.id)
        for profile in profiles:
            profile_id = profile.id
        obj = Profile.objects.get(id=profile_id)
        self.extra_context = {'avatar': obj.avatar}

        return obj


class StudentDelete(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'students/student_delete.html'
    login_url = reverse_lazy('students:login')
    success_url = reverse_lazy('students:list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.extra_context = {'name': obj.full_name()}

        return obj


class PageNotFound(TemplateView):
    template_name = 'errors/404.html'


class RegistrationStudent(CreateView):
    form_class = RegistrationStudentForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy('students:sent-email')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        send_registration_email(request=self.request,
                                user_instance=self.object)
        return super().form_valid(form)


class UserLogin(LoginView):
    pass


class LogoutStudent(LogoutView):
    template_name = 'registration/logged_out.html'


class ActivateUser(RedirectView):

    def get(self, request, uidb64, token, *args, **kwargs):

        try:
            user_pk = force_bytes(urlsafe_base64_decode(uidb64))
            current_user = CustomUser.objects.get(pk=user_pk)
        except (CustomUser.DoesNotExist, ValueError, TypeError):
            return HttpResponse("Wrong data")

        if current_user and TokenGenerator().check_token(current_user, token):
            current_user.is_active = True
            current_user.save()
            profile = Profile.objects.get(user_id=current_user.id)
            self.url = reverse_lazy('students:update', kwargs={'pk': profile.id})

            login(request, current_user)
            return super().get(request, *args, **kwargs)
        return HttpResponse("Wrong data")


class ActivateSentEmail(TemplateView):
    template_name = 'emails/activate_email_sent.html'
