from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from asrlab.settings import ZONE_INFO
from chatapp.forms import SessionNameForm
from chatapp.models import Conversation, Message
from users.mixin import LoginRequiredMixin


class ChatBotView(LoginRequiredMixin, View):
    def get(self, request):
        # 会话信息
        sessionsList = Conversation.objects.filter(username=request.user) \
            .order_by("-startTime").values("sessionId", "sessionName")

        return render(request, "app-chat.html", {
            "ws_url": "ws://%s/chatapp/ws/" % request.headers['Host'],
            "sessionsList": sessionsList,
        })


class ChatHistoriesView(LoginRequiredMixin, View):
    def get(self, request):
        currentSessionId = request.GET.get("sessionId")
        messages = Message.objects.filter(conversation__sessionId=currentSessionId)
        if len(messages) == 1:
            # 消息不为空
            return JsonResponse({"status": "success", "content": messages[0].content})
        else:
            # 只有一个会话
            session = Conversation.objects.filter(sessionId=currentSessionId)
            if len(session) == 0:
                return JsonResponse({"status": "reload", "content": "null"})

        # 消息为空
        return JsonResponse({"status": "empty", "content": "null"})


class AddSessionView(LoginRequiredMixin, View):
    def post(self, request):
        nameForm = SessionNameForm(request.POST)
        if nameForm.is_valid():
            newSession = Conversation(
                username=request.user,
                sessionName=request.POST.get("sessionName")
            )
            newSession.save()
            return JsonResponse({
                "status": "success",
                "message": "创建成功",
                "id": newSession.sessionId,
                "name": newSession.sessionName,
                "startTime": newSession.startTime.astimezone(ZONE_INFO).strftime("%Y年%m月%d日 %H:%M:%S")
            })

        return JsonResponse({"status": "error", "message": "会话名称太长 (10字以内)"})


class ModifySessionNameView(LoginRequiredMixin, View):
    def post(self, request):
        nameForm = SessionNameForm(request.POST)
        if nameForm.is_valid():
            modifySession = Conversation.objects.get(username=request.user, sessionId=request.POST.get("sessionId"))
            modifySession.sessionName = request.POST.get("sessionName")
            modifySession.save()
            return JsonResponse({
                "status": "success",
                "message": "修改成功",
                "id": modifySession.sessionId,
                "name": modifySession.sessionName
            })

        return JsonResponse({"status": "error", "message": "会话名称太长 (10字以内)"})


class RemoveSessionView(LoginRequiredMixin, View):
    def post(self, request):
        removeSession = Conversation.objects.filter(username=request.user, sessionId=request.POST.get("sessionId"))
        if len(removeSession) == 1:
            removeSession[0].delete()
            return JsonResponse({"status": "success", "message": "删除成功"})

        return JsonResponse({"status": "error", "message": "删除失败"})
