from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from catalog.utils.mixins import StyleFormMixin
from users.models import User


class RegisterUserCreationForm(StyleFormMixin, UserCreationForm):
    FIELDS_WITH_ATTRIBUTES = {
        "email": {"class": "form-control", "placeholder": "Введите email"},
        "avatar": {"class": "form-control"},
        "phone_number": {"class": "form-control", "placeholder": "Формат: +7 999 666 33 33"},
        "country": {"class": "form-control", "placeholder": "Введите страну"},
    }

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль"}),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Повторите пароль"}),
    )

    class Meta:
        model = User
        fields = ["email", "avatar", "phone_number", "country", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Введите email",
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = "Пароль"
        self.fields["password"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите пароль",
        })


class UserForm(StyleFormMixin, forms.ModelForm):
    FIELDS_WITH_ATTRIBUTES = {
        "avatar": {"class": "form-control"},
        "phone_number": {"class": "form-control", "placeholder": "Формат: +7 999 666 33 33"},
        "country": {"class": "form-control", "placeholder": "Введите страну"},
    }

    class Meta:
        model = User
        fields = ["avatar", "phone_number", "country"]
