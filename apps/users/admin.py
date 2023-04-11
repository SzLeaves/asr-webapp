from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from users.models import UserProfile, EmailVerifyRecord
from users.resource import UserProfileResource, VerifyRecordResource


class UserProfileAdmin(ImportExportModelAdmin):
    list_display = ("id", "username", "email")
    list_filter = ["id", "username", "email"]
    search_fields = ["id", "username", "email"]
    resource_class = UserProfileResource


class EmailVerifyRecordAdmin(ImportExportModelAdmin):
    list_display = ("addressee", "sendType", "sendTime", "code")
    search_fields = ["email", "sendType", "sendTime", "code"]
    resource_class = VerifyRecordResource


# 注册模型
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

# admin界面设置
# 页面标题
admin.site.site_header = "ASR Lab 后台管理"
# 标签栏标题
admin.site.site_title = "ASR Lab - 后台管理系统"
