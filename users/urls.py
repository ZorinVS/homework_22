from django.contrib.auth.views import LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user-update/<int:pk>/", views.UserUpdateView.as_view(), name="user_update"),
]
