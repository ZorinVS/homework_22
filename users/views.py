from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView

from config.settings import EMAIL_HOST_USER
from users import forms
from users.models import User


class LoginView(BaseLoginView):
    form_class = forms.LoginForm
    template_name = "users/login.html"


class RegisterView(FormView):
    form_class = forms.RegisterUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    @staticmethod
    def send_welcome_email(user_email):
        subject = "Добро пожаловать в наш сервис"
        message = "Спасибо, что зарегистрировались в нашем сервисе!"
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.UserForm
    success_url = reverse_lazy("catalog:home")
