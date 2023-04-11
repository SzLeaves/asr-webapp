import os
import time
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from asrlab.settings import MEDIA_ROOT, ZONE_INFO
from asrlab.settings import logger
from sttapp.forms import SpeechToTextForm
from sttapp.models import SpeechToText
from users.mixin import LoginRequiredMixin
from utils.predict import decodeAndPredict


class SpeechToTextView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "app-stt.html")

    def post(self, request):
        file_form = SpeechToTextForm(request.POST, request.FILES)
        if file_form.is_valid():
            # 保存文件
            processRecord = SpeechToText(username=request.user,
                                         fileName=file_form.cleaned_data['fileName'],
                                         filePath=file_form.cleaned_data['filePath'])
            processRecord.save()
            filePath = MEDIA_ROOT + str(processRecord.filePath)

            try:
                startTime = time.time()
                logger.info(request.user.email + " 正在转换音频")
                # 预测结果
                predictText = decodeAndPredict(filePath)
                endTime = time.time() - startTime

                # 保存处理记录
                processRecord.finishTime = datetime.now(ZONE_INFO)
                processRecord.times = endTime
                processRecord.content = predictText
                processRecord.save()
                logger.info(request.user.email + " 转换完成")

            except Exception as e:
                logger.error(e)
                return JsonResponse({"status": "error"})
            finally:
                # 删除文件
                os.remove(filePath)

            return JsonResponse({"status": "success", "text": predictText})

        return JsonResponse({"status": "error"})


class DeleteHistoriesView(LoginRequiredMixin, View):
    def post(self, request):
        recordId = request.POST.get("id")
        try:
            deleteRecord = SpeechToText.objects.get(username=request.user, id=recordId)
            deleteRecord.delete()
            return JsonResponse({"status": "success", "message": "删除成功", "id": recordId})

        except Exception as e:
            logger.error(e)
            return JsonResponse({"status": "error", "message": "删除失败"})
