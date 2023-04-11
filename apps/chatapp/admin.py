from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from chatapp.models import Conversation, Message
from chatapp.resource import ConversationResource, MessageResource


class ConversationAdmin(ImportExportModelAdmin):
    list_display = ("sessionId", "username", "startTime", "endTime")
    list_filter = ("username", "startTime", "endTime")
    search_fields = ("username",)
    resource_class = ConversationResource


class MessageResourceAdmin(ImportExportModelAdmin):
    list_display = ("conversation",)
    list_filter = ("conversation",)
    search_fields = ("conversation",)
    resource_class = MessageResource


# 注册模型
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageResourceAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "ASR Lab 后台管理"
# 标签栏标题
admin.site.site_title = "ASR Lab - 后台管理系统"
