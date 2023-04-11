from django.apps import AppConfig

import utils.loader


class UtilsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "utils"

    def ready(self):
        # 启动时加载数据
        utils.loader.loadData()
