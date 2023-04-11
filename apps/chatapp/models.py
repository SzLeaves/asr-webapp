import uuid

from django.db import models

from users.models import UserProfile


def getUniqueId():
    return str(uuid.uuid1())


class Conversation(models.Model):
    sessionId = models.CharField(primary_key=True, max_length=50, default=getUniqueId, verbose_name="会话ID")
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户信息")
    sessionName = models.CharField(max_length=10, default="新会话", verbose_name="会话名称")
    startTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    endTime = models.DateTimeField(null=True, blank=True, verbose_name="上次访问时间")

    class Meta:
        verbose_name = "聊天会话"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username.email


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, verbose_name="会话信息")
    content = models.JSONField(verbose_name="消息内容", null=True)

    class Meta:
        verbose_name = "聊天消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.conversation.username.email
