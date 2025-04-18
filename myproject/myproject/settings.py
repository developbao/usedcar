"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import mongoengine
import os
from pathlib import Path
from gridfs import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#w1_awh@g@l*i)63oiw6z^ko1x0&@_kp)t@)2tpxb7#cukx&yg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'users',
    'recommendation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users', 'templates', 'users')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# mongo_con = mongoengine.connect('all_database', host = '120.53,220.118', port = 27000)
# mongo_db = mongo_con.all_database
# fs = GridFS(mongo_db, collection = 'car_collection') # mongo 图片连接

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongodb': {
        'DATABASE': 'all_database',
        'USER_COLLECTION': 'user_collection',
        'CAR_COLLECTION': 'car_collection',
        'HOST': '47.121.190.121',
        'PORT': 27000
    }
}

# STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')
# STATIC_ROOT_IMG = os.path.join(os.path.dirname(__file__), 'static/images')
# STATICFILES_DIRS = ( ('css',os.path.join(STATIC_ROOT,'css').replace('\\','/') ), 
#                     ('js',os.path.join(STATIC_ROOT,'js').replace('\\','/') ), 
#                     ('images',os.path.join(STATIC_ROOT,'images').replace('\\','/') ), 
#                     ('upload',os.path.join(STATIC_ROOT,'upload').replace('\\','/') )
#                     ) #django静态文件加载路径


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

USE_L10N = True

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# 配置静态文件的目录，确保 Django 能找到你的 static 文件
STATICFILES_DIRS = [
    BASE_DIR / "users" / "static",  # 修改为指向 'users/static'
    BASE_DIR / "static",
]

# 在生产环境中，Django 会将静态文件收集到 STATIC_ROOT 目录
STATIC_ROOT = BASE_DIR / "staticfiles"  # 只在生产环境中使用
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
