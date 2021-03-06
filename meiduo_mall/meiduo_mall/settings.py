"""
Django settings for meiduo_mall project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o93qf^plxph1i+zz3_mf@l!-@g651%zs+!7tu(fk(hz6ylrdvn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'www.meiduo.site']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users.apps.UsersConfig',
    'apps.verification',
    'apps.oauth',
    'apps.areas'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meiduo_mall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'temples')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meiduo_mall.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo_mall',  # 数据库名称
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 端口号
        'USER': 'meiduouser',  # 数据库账号
        'PASSWORD': '123456'  # 数据库密码
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8081',
)

# 配置缓存
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": '12345'
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": '12345'
        }
    },
    "code": {  # 验证码
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": '12345'
        }
    },

}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"  # 表示session采⽤缓存⽅式保存
SESSION_CACHE_ALIAS = "session"  # 表示使⽤缓存的地⽅是redis的session配置节点

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁⽤已经存在的⽇志器
    'formatters': {  # ⽇志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对⽇志进⾏过滤
        'require_debug_true': {  # django在debug模式下才输出⽇志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # ⽇志处理⽅法
        'console': {  # 向终端中输出⽇志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向⽂件中输出⽇志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/meiduo.log'),  # ⽇志⽂件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # ⽇志器
        'django': {  # 定义了⼀个名为django的⽇志器
            'handlers': ['console', 'file'],  # 可以同时向终端与⽂件中输出⽇志
            'propagate': True,  # 是否继续传递⽇志信息
            'level': 'INFO',  # ⽇志器接收的最低⽇志级别
        },
    }
}
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CELERY_BROKER_URL="redis://:12345@127.0.0.1/3"
CELERY_RESULT_BACKEND="redis://:12345@127.0.0.1/4"

# QQ登录参数
# 我们申请的 客户端id
QQ_CLIENT_ID ='101474184'
# 我们申请的 客户端秘钥
QQ_CLIENT_SECRET ='c6ce949e04e12ecc909ae6a8b09b637c'
# 我们申请时添加的: 登录成功后回调的路径
QQ_REDIRECT_URI ='http://www.meiduo.site:8080/oauth_callback.html'
QQ_STATE ='meiduosite'

# 邮件后端配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 与SMTP服务器通信的地址
EMAIL_HOST = 'smtp.office365.com'
# 与SMTP服务器通信使用的端口号
EMAIL_PORT = 587
# 与SMTP服务器登录的用户名
EMAIL_HOST_USER = 'turboyuhui@outlook.com'
# 与SMTP服务器登录的密码
EMAIL_HOST_PASSWORD = 'huiqihang.0207'
# 发件人地址
EMAIL_FROM = 'turbo<turboyuhui@outlook.com>'
# 与SMTP服务器通信使用的TLS加密方式
EMAIL_USE_TLS = 'STARTTLS'

EMAIL_VERIFY_URL = 'http://www.meiduo.site:8080/success_verify_email.html'

