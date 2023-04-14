from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from asrlab.settings import EMAIL_HOST_USER
from users.models import EmailVerifyRecord


class MailSender:

    def __init__(self, addressee, title, sendType, template, callbackPath):
        self.emailRecord = EmailVerifyRecord(addressee=addressee, sendType=sendType)
        self.title = title
        self.addressee = addressee
        self.sendType = sendType
        self.template = template
        self.callbackPath = callbackPath

    def sendMail(self):
        """
        发送验证邮件
        """
        # 生成验证码
        path = ""
        if self.sendType == 'register':
            path = self.callbackPath + "/user/active/"
        elif self.sendType == 'forget':
            path = self.callbackPath + "/user/reset/"

        # 存入数据库用于后续查询
        self.emailRecord.save()

        # 发送邮件
        sender = EmailMultiAlternatives(
            subject=self.title,
            body="ASR Lab 用户: %s  链接: %s" % (self.addressee, self.emailRecord.code),
            from_email=EMAIL_HOST_USER,
            to=[self.addressee],
        )

        # 指定邮件模板
        sender.attach_alternative(self.getTemplate(path), "text/html")
        sender.send()

    def getTemplate(self, path):
        """
        读取发送邮件模板
        """
        renderContext = {"addressee": self.addressee, "code": path + self.emailRecord.code}
        return render_to_string(self.template, renderContext)
