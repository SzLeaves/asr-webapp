from django.urls import path, re_path

from users.views import UserForgotPasswordView, UserResetPasswordView, UserSettingsView
from users.views import UserLoginView, UserLogoutView, UserRegisterView, UserActiveView

app_name = "apps.users"
urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("forget/", UserForgotPasswordView.as_view(), name="forget"),
    path("settings/", UserSettingsView.as_view(), name="settings"),
    re_path("reset/(?P<verify_code>.*)", UserResetPasswordView.as_view(), name="reset"),
    re_path("active/(?P<verify_code>.*)/", UserActiveView.as_view(), name="active"),
]
