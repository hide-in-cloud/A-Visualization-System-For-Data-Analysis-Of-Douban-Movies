"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os.path
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d!30t!jubd9m0j8&=r)opz%)3yn93xurzdhq*w#tr3i-k#=5y='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'app.apps.AppConfig',
    'rest_framework',
    'corsheaders',  # 跨域注册
    'django_filters',   # 模糊查询
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 跨域
]

ROOT_URLCONF = 'djangoProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
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

WSGI_APPLICATION = 'djangoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'douban_movie',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS':{
            # 严格模式
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'  # 设置中文

TIME_ZONE = 'Asia/Shanghai'  # 中国时区

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 媒体文件地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# 跨域支持
# CORS_ALLOWED_ORIGINS = ['http://127.0.0.1:9528']  # 授权进行跨站点 HTTP 请求的源列表
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有的元访问
CORS_ALLOW_HEADERS = ('*') #允许所有的请求头
# 因为跨域之后需要传递sessionid 到浏览器cookie，所以添加如下配置。
CORS_ALLOW_CREDENTIALS = True  # 允许 Cookie 包含在跨站点 HTTP 请求中
SESSION_COOKIE_SAMESITE = None  # django 自己的安全策略

# 权限设置
PERMISSION = {
    'admin':{
        'movie/info-list':['GET','POST'],
        'movie/info-detail':['GET','PUT','PATCH','DELETE'],
        'movie/info-homeInfo':['GET'],
        'movie/page-list':['GET','POST'],
        'movie/page-detail':['GET','PUT','PATCH','DELETE'],
        'userByPage-list':['GET','POST','PUT','PATCH','DELETE'],
    },
    'user':{
        'movie/info-list':['GET'],
        'movie/info-detail':['GET'],
        'movie/info-homeInfo':['GET'],
        'movie/page-list':['GET'],
        'movie/page-detail':['GET'],
    },
}


# 全局使用，配置在配置文件中
REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': [  # 全局使用，所有接口都必须登录才能用
    #     'app.auth.LoginAuth'
    # ],

    # 全局异常处理
    'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
    # 修改Json返回的数据格式
    'DEFAULT_RENDERER_CLASSES':(
        'utils.customRenderer.MyJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}
