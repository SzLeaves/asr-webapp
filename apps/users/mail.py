import random

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from asrlab.settings import EMAIL_HOST_USER
from users.models import EmailVerifyRecord


class MailSender:
    # 字符集(用于随机生成)
    urlCharset = "".join([chr(i) for i in range(65, 65 + 26)] +
                         [chr(i) for i in range(97, 97 + 26)] +
                         [str(i) for i in range(10)])

    def __init__(self, addressee, title, sendType, template, callbackPath):
        self.emailRecord = None
        self.title = title
        self.addressee = addressee
        self.sendType = sendType
        self.template = template
        self.callbackPath = callbackPath

    def sendMail(self):
        """
        发送验证邮件
        """
        # 创建验证邮件对象
        self.emailRecord = EmailVerifyRecord()
        self.emailRecord.addressee = self.addressee
        self.emailRecord.sendType = self.sendType
        path = ""

        # 生成验证码
        if self.sendType == 'update':
            # 用于用户信息界面修改邮箱的确认身份验证码, 取四位便于输入
            self.emailRecord.code = MailSender.getRandomString()[:4]
        else:
            self.emailRecord.code = MailSender.getRandomString()
            if self.sendType == 'register':
                path = self.callbackPath + "/user/active/"
            elif self.sendType == 'forget':
                path = self.callbackPath + "/user/reset/"

        # 存入数据库用于后续查询
        self.emailRecord.save()

        # 邮件信息
        emailContent = self.getTemplate(path)

        # 发送邮件
        sender = EmailMultiAlternatives(
            subject=self.title,
            body="Your device does not support HTML mail.",
            from_email=EMAIL_HOST_USER,
            to=[self.addressee],
        )

        sender.attach_alternative(emailContent, "text/html")
        sender.send()

    def getTemplate(self, path):
        """
        读取发送邮件模板
        """
        renderContext = {"addressee": self.addressee, "code": path + self.emailRecord.code}
        return render_to_string(self.template, renderContext)

    @staticmethod
    def getRandomString(length=15):
        """
        生成指定长度的随机字符串
        """
        randomString = ""
        for ch in range(len(MailSender.urlCharset)):
            randomString += MailSender.urlCharset[random.randint(0, len(MailSender.urlCharset) - 1)]
        return randomString[:length]
