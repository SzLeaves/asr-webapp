from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
    登录界面表单检查
    """
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)


class ForgetPasswordForm(forms.Form):
    """
    忘记密码界面表单检查
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    """
    注册界面表单检查
    """
    email = forms.EmailField(required=True)
    password_1 = forms.CharField(required=True, min_length=5)
    password_2 = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()

    # 检验两次密码一致
    def clean(self):
        if self.cleaned_data.get('password_1') != self.cleaned_data.get('password_2'):
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


class ResetPasswordForm(forms.Form):
    """
    密码重置表单检查
    """
    password_1 = forms.CharField(required=True, min_length=5)
    password_2 = forms.CharField(required=True, min_length=5)

    # 检验两次密码一致
    def clean(self):
        if self.cleaned_data.get('password_1') != self.cleaned_data.get('password_2'):
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


class UserInfoResetPasswordForm(forms.Form):
    """
    密码重置表单检查
    """
    password_1 = forms.CharField(required=True, min_length=5)
    password_2 = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()

    # 检验两次密码一致
    def clean(self):
        if self.cleaned_data.get('password_1') != self.cleaned_data.get('password_2'):
            raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data
