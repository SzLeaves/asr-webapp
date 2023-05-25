from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from asrlab.settings import logger
from utils.mail import MailSender
from chatapp.models import Conversation
from sttapp.models import SpeechToText
from users.forms import LoginForm, ForgetPasswordForm, RegisterForm
from users.forms import ResetPasswordForm, UserInfoResetPasswordForm
from users.mixin import LoginRequiredMixin
from users.models import UserProfile, EmailVerifyRecord

"""
# 用户管理相关操作 #
"""


class CustomBackend(ModelBackend):
    """
    auth 自定义表单验证逻辑
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 模型数据取并集
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            logger.error(e)
            return None


class UserLoginView(View):
    """
    用户登录功能逻辑
    """

    def get(self, request):
        # 检查是否已登录, 重定向至app页面
        if request.user.is_authenticated:
            return redirect("sttapp:app")

        # 生成验证码
        captchaForm = ForgetPasswordForm()
        return render(request, "login-index.html", {"captchaForm": captchaForm})

    def post(self, request):
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            email = request.POST.get("email", "")
            password = request.POST.get("password", "")
            # 验证记录
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    # 登录成功
                    login(request, user)
                    return JsonResponse({"status": "success", "message": "登录成功"})
                else:
                    return JsonResponse({"status": "error", "message": "账号未激活"})

        return JsonResponse({"status": "error", "message": "账户不存在或密码错误"})


class UserLogoutView(View):
    """
    用户注销逻辑
    """

    def get(self, request):
        logout(request)
        return redirect("users:login")


class UserForgotPasswordView(View):
    """
    用户找回密码界面功能逻辑
    """

    def post(self, request):
        forgetPasswordForm = ForgetPasswordForm(request.POST)
        if forgetPasswordForm.is_valid():
            # 判断用户是否存在
            email = request.POST.get("email", "")
            isUserExist = len(UserProfile.objects.filter(email=email)) == 1
            if isUserExist:
                # 发送邮件
                sender = MailSender(email, "重置密码", "forget",
                                    "mail-forget.html", request.headers['Host'])
                sender.sendMail()
                return JsonResponse({"status": "success", "message": "重置链接已发送至邮箱"})
            else:
                return JsonResponse({"status": "error", "message": "用户不存在"})

        return JsonResponse({"status": "error", "message": "邮箱或验证码错误"})


class UserResetPasswordView(View):
    """
    用户重置密码界面功能逻辑
    """

    def get(self, request, verify_code):
        savedRecord = EmailVerifyRecord.objects.filter(code=verify_code)
        if len(savedRecord) == 1:
            user = UserProfile.objects.get(email=savedRecord[0].addressee)
            return render(request, "login-reset.html", {"email": user.email})

        # 验证码失效时重定向回登录页
        return redirect("users:login")

    def post(self, request, verify_code):
        savedRecord = EmailVerifyRecord.objects.filter(code=verify_code)
        if len(savedRecord) == 1:
            logout(request)
            resetForm = ResetPasswordForm(request.POST)
            if resetForm.is_valid():
                password = request.POST.get("password_1")
                # 更新密码 (加密为hash后保存)
                user = UserProfile.objects.get(email=savedRecord[0].addressee)
                user.password = make_password(password)
                user.save()
                # 删除验证码记录
                savedRecord.delete()
                return JsonResponse({"status": "success", "message": "密码重置成功, 请重新登录"})
            else:
                return JsonResponse({"status": "error", "message": "两次密码不一致"})

        # 验证码失效时重定向回登录页
        return redirect("users:login")


class UserRegisterView(View):
    """
    用户注册功能逻辑
    """

    def get(self, request):
        captchaForm = RegisterForm()
        return render(request, "login-register.html", {"captchaForm": captchaForm})

    def post(self, request):
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            email = request.POST.get("email", "")
            isUserExist = len(UserProfile.objects.filter(email=email)) == 1
            if not isUserExist:
                password = request.POST.get("password_1", "")
                # 新建用户
                newUser = UserProfile(email=email, password=make_password(password), username=email)
                newUser.is_active = False
                # 发送激活邮件
                sender = MailSender(email, "激活账户", "register",
                                    "mail-register.html", request.headers['Host'])
                sender.sendMail()
                # 保存用户
                newUser.save()
                return JsonResponse({"status": "success", "message": "激活链接已发送至邮箱"})
            else:
                return JsonResponse({"status": "error", "message": "用户已存在"})

        return JsonResponse({"status": "error", "message": "邮箱, 密码或验证码格式错误"})


class UserActiveView(View):
    """
    用户激活功能逻辑
    """

    def get(self, request, verify_code):
        logout(request)
        savedRecord = EmailVerifyRecord.objects.filter(code=verify_code)
        if len(savedRecord) == 1:
            # 获取验证码对应邮箱
            email = savedRecord[0].addressee
            # 获取邮箱对应用户
            user = UserProfile.objects.filter(email=email)
            if len(user) == 1:
                # 激活用户
                user[0].is_active = True
                user[0].save()
                # 使当前验证码失效
                savedRecord.delete()

                return render(request, "login-index.html", {"message": "账号激活成功, 请稍后"})

        # 验证码失效时重定向回登录页
        return redirect("users:login")


class UserSettingsView(LoginRequiredMixin, View):
    """
    设置界面逻辑
    """

    def get(self, request):
        # 获取转换记录
        histories = SpeechToText.objects.filter(username=request.user) \
            .order_by("-handleTime").values("id", "fileName", "handleTime", "content", "times")
        # 获取会话记录
        sessions = Conversation.objects.filter(username=request.user) \
            .order_by("-startTime").values("sessionId", "sessionName", "startTime", "endTime")

        # 初始化验证表单
        infoCaptchaForm = UserInfoResetPasswordForm()
        return render(request, "app-settings.html", {
            "infoCaptchaForm": infoCaptchaForm,
            "histories": histories,
            "sessions": sessions,
        })

    def post(self, request):
        infoCaptchaForm = UserInfoResetPasswordForm(request.POST)
        if infoCaptchaForm.is_valid():
            password = request.POST.get("password_1")
            # 更新密码 (加密为hash后保存)
            user = UserProfile.objects.get(email=request.user.email)
            user.password = make_password(password)
            user.save()

            # 注销用户
            logout(request)
            return JsonResponse({"status": "success", "message": "密码重置成功, 请重新登录"})
        else:
            return JsonResponse({"status": "error", "message": "两次密码不一致或验证码错误"})
