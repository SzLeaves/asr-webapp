from datetime import datetime

from django.db import models

from users.models import UserProfile


class SpeechToText(models.Model):
    """
    语音转文字处理数据模型
    """

    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户信息")
    fileName = models.CharField(max_length=512, verbose_name="处理音频名称", null=False)
    filePath = models.FileField(
        max_length=128, upload_to="audios/%Y/%m", verbose_name="处理音频路径", null=False
    )
    handleTime = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    finishTime = models.DateTimeField(verbose_name="完成时间", null=True)
    content = models.TextField(verbose_name="转换内容", null=True, default="")
    times = models.IntegerField(verbose_name="转换时长", null=True, default=0)

    class Meta:
        verbose_name = "处理任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.fileName
