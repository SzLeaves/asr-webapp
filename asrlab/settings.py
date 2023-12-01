import json
import logging
import os
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from django_redis import get_redis_connection
from sshtunnel import SSHTunnelForwarder

os.environ['DJANGO_SETTINGS_MODULE'] = 'asrlab.settings'

# 读取配置文件
with open("config.json", "r") as file:
    CONFIG = json.load(file)

# 将自定义apps模块添加到启动环境中
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))

SECRET_KEY = "django-insecure-91b63r@0v2_dgplv1mx%*a+fq8oookyq@mzq8j*y&8(1ld#)2$"
DEBUG = True

# 日志输出模块设置
LOGGING = {
    'version': 1,
    'encoding': 'utf-8',
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
            'level': 'INFO',
        },
    },
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s[%(asctime)s %(levelname)s]'
                      ' %(module)s:%(funcName)s:%(lineno)s - %(reset)s%(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            },
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logger = logging.getLogger("django")

ALLOWED_HOSTS = ['*']

# 需要使用的app模块
INSTALLED_APPS = [
    "daphne",
    "simpleui",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.conf",
    "import_export",
    "captcha",
    'channels',
    "apps.utils",
    "apps.users",
    "apps.sttapp",
    "apps.chatapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "asrlab.urls"

# 模板设置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # 添加模板文件夹路径
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 静态文件路径
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# 上传文件路径
MEDIA_URL = "upload/"
MEDIA_ROOT = os.path.join(BASE_DIR, "upload/")

ASGI_APPLICATION = "asrlab.asgi.application"

# 数据库配置

# MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "asrapp",
        "HOST": CONFIG['DATABASE']['MYSQL']['HOST'],
        "PORT": CONFIG['DATABASE']['MYSQL']['PORT'],
        "USER": CONFIG['DATABASE']['MYSQL']['USER'],
        "PASSWORD": CONFIG['DATABASE']['MYSQL']['PASSWORD'],
    }
}

# Redis cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://%s:%d/0" % (CONFIG['DATABASE']['REDIS']['HOST'], CONFIG['DATABASE']['REDIS']['PORT']),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": CONFIG['DATABASE']['REDIS']['PASSWORD'],
        }
    }
}
REDIS_POOL = get_redis_connection()

# Redis channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ["redis://:%s@%s:%d/1" % (
                CONFIG['DATABASE']['REDIS']['PASSWORD'],
                CONFIG['DATABASE']['REDIS']['HOST'],
                CONFIG['DATABASE']['REDIS']['PORT'],
            )]
        },
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# auth模块配置
AUTH_USER_MODEL = "users.UserProfile"  # 指定需要使用auth模块的自定义Model
AUTHENTICATION_BACKENDS = (
    'apps.users.views.CustomBackend',
)
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# cookies失效时间 7天
SESSION_COOKIE_AGE = 604800

# 设置语言/时区环境
LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"
TIME_FORMAT = "%Y/%m/%d %H:%M:%S"
ZONE_INFO = ZoneInfo(TIME_ZONE)

USE_I18N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# admin import_export设置
IMPORT_EXPORT_USE_TRANSACTIONS = True

# admin 界面主题
SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False
SIMPLEUI_DEFAULT_THEME = "light.css"

# 邮件服务器设置
EMAIL_HOST = CONFIG['EMAIL']['HOST']
EMAIL_PORT = CONFIG['EMAIL']['PORT']
EMAIL_HOST_USER = CONFIG['EMAIL']['USER']
EMAIL_HOST_PASSWORD = CONFIG['EMAIL']['PASSWORD']
EMAIL_USE_TLS = False

# 音频数据权重路径
DATA_WEIGHT_PATH = BASE_DIR / "data" / "data_weight.pkl"
# 词库数据路径
DICT_PATH = BASE_DIR / "data" / "words_vec.pkl"
# 语音识别模型路径
ASR_MODEL_PATH = BASE_DIR / "data" / "asr_models" / "model.h5"
# 标点符号模型路径
PUN_MODEL_PATH = BASE_DIR / "data" / "pun_models"

# Bot API
BOT_API_URL = CONFIG['BOT']['API_URL']
# API headers
BOT_API_HEADERS = {
    'Authorization': 'Bearer %s' % CONFIG['BOT']['API_KEY'],
    'Connection': 'keep-alive',
    'Content-Type': 'application/json'
}
