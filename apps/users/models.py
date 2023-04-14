import random
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# 字符集(用于随机生成)
urlCharset = "".join([chr(i) for i in range(65, 65 + 26)] +
                     [chr(i) for i in range(97, 97 + 26)] +
                     [str(i) for i in range(10)])


def getRandomString(length=15):
    """
    生成指定长度的随机字符串
    """
    randomString = ""
    for ch in range(len(urlCharset)):
        randomString += urlCharset[random.randint(0, len(urlCharset) - 1)]
    return randomString[:length]


"""
# 用户管理数据模型 #
"""


class UserProfile(AbstractUser):
    """
    用户信息数据模型
    """
    nickname = models.CharField(max_length=10, null=True, blank=True, default="", verbose_name="用户昵称")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    """
    邮箱验证码数据模型
    """

    code = models.CharField(max_length=20, verbose_name="验证码", null=False, blank=False, default=getRandomString)
    addressee = models.EmailField(verbose_name="收件人邮箱", null=False, blank=False, default="")
    sendTime = models.DateTimeField(verbose_name="发送时间", default=datetime.now)
    sendType = models.CharField(
        choices=(("register", "注册"), ("forget", "找回密码")),
        max_length=10,
        verbose_name="验证类型",
    )

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s (%s)" % (self.addressee, self.code)
