from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from sttapp.models import SpeechToText
from sttapp.resource import SpeechToTextResource


class SpeechToTextAdmin(ImportExportModelAdmin):
    list_display = ("username", "fileName", "filePath", "handleTime")
    list_filter = ("username", "fileName", "filePath", "handleTime")
    search_fields = ("username", "fileName", "filePath", "handleTime")
    resource_class = SpeechToTextResource


# 注册模型
admin.site.register(SpeechToText, SpeechToTextAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "ASR Lab 后台管理"
# 标签栏标题
admin.site.site_title = "ASR Lab - 后台管理系统"
