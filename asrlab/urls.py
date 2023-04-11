from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from apps.users.views import UserLoginView
from asrlab.settings import MEDIA_ROOT

urlpatterns = [
    # 后台管理
    path("admin/", admin.site.urls),
    # 验证码
    path("captcha/", include("captcha.urls")),

    # 主页
    path("", UserLoginView.as_view(), name="index"),

    # 用户管理
    path("user/", include("apps.users.urls", namespace="users")),

    # STT lab
    path("sttapp/", include("apps.sttapp.urls", namespace="sttapp")),

    # Chat lab
    path("chatapp/", include("apps.chatapp.urls", namespace="chatapp")),

    # 上传文件
    re_path("^upload/(?P<path>.*)", serve, {"document_root": MEDIA_ROOT}),
]
