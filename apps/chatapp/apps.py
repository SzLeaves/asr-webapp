from django.apps import AppConfig


class ChatappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chatapp"
    verbose_name = "语音聊天机器人"
