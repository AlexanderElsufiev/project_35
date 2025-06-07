
from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uqg0t6)jqhp5^h2kx5c9qd30-t1&^t!7a$3jkgo5#7mu12w-mr'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']



# ДОБАВКА
STATICFILES_DIRS = [
    BASE_DIR / "static"
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # добавил
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django_filters',

    'django_dump_load_utf8', # ЧТОБЫ УМЕЛ СОХРАНТЬ ДАННЫЕ В РАЗНЫХ КОДИРОВКАХ, ВТЧ КИРИЛЛИЦУ

    # ДОБАВКА ДЛЯ ВОЗМОЖНОСТИ ИДЕНТИФИКАЦИИ ПОЛЬЗОВАТЕЛЕЙ
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    # ДЛЯ ЯНДЕКСА
    'allauth.socialaccount.providers.yandex',
    'sign',
    'protect',
    'appointment',
    # 'news',  # меняю .ту строку на следующую, чтобы работали сигналы для почты
    'news.apps.NewsConfig',
    'django_apscheduler', # ЭТО ДЛЯ ПЕРИОДИЧЕСКИХ ЗАДАЧ
    # 'mathfilters', # МАТЕМАТИЧЕСКИЕ ФОРМУЛЫ ДЛИННЫЕ

]

# ЭТО ДЛЯ ПЕРИОДИЧЕСКИХ ЗАДАЧ
# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds #=ЧЕРЕЗ СКОЛЬКО ВРЕМЕНИ СНИМАЕТСЯ ЗАДАЧА, КОТОРАЯ НЕ ОТВЕЧАЕТ


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ДЛЯ КЭШИРОВАНИЙ САЙТА ЦЕЛИКОМ - ПО ИНСТРУКЦИИ ИДЁТ СРАЗУ ПОСЛЕ СЕКРЕТНОСТИ
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware: - необходима для версий django-allauth 0.55.0.
    "allauth.account.middleware.AccountMiddleware",

    # ДЛЯ ЛОКАЛИЗАЦИИ
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'

]



ROOT_URLCONF = 'project.urls'

# LOGIN_URL = 'sign/login/' - старый вариант затираем
LOGIN_URL = '/accounts/login/'

# LOGIN_REDIRECT_URL = '/' #ЭТО ПОСЛЕ АВТОРИЗАЦИИ ВЕЛО НА http://127.0.0.1:8000/
# LOGIN_REDIRECT_URL = '/news/' #ЭТО ПОСЛЕ АВТОРИЗАЦИИ ВЕДЁТ НА http://127.0.0.1:8000/news/
LOGIN_REDIRECT_URL = '/' #ЭТО ПОСЛЕ АВТОРИЗАЦИИ ВЕДЁТ НА КОРНЕВУЮ СТРАНИЦУ ПОЛЬЗОВАТЕЛЯ


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

SITE_ID = 1
SITE_URL='http://127.0.0.1:8000/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'DIRS': [BASE_DIR/'templates'],
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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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



TIME_ZONE = 'UTC'

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # ЧТОБЫ ОТПРАВКА ПИСЕМ БЫЛА РЕАЛЬНОЙ - не проходит по таймауту!
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # не отправка реальная. а проверка в консоли

EMAIL_USE_TLS = False
EMAIL_USE_SSL = True  # Яндекс использует ssl, подробнее о том, что это, почитайте в дополнительных источниках, но включать его здесь обязательно
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый

# БЛОК ПОДХВАТА ИЗ СЕКРЕТНОЙ ЧАСТИ
import os
from dotenv import load_dotenv
load_dotenv()
EMAIL_HOST = os.getenv('EMAIL_HOST')
# EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# DEFAULT_FROM_EMAIL = 'settings_default@mail.ru'

# ВВОДИМ ЧТОБЫ ОТПРАВЛЯЛИСЬ ПИСЬМА ПРИ РЕГИСТРАЦИИ
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'





# ДЛЯ РАБОТЫ ЛОКАЛИЗАЦИИ ОТКЛЮЧАЮ КЕШИРОВАНИЕ
# CACHES = {
#     'default': {
#         # 'TIMEOUT': 60,
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
#     }
# }


# ВСЁ ДЛЯ ЛОГИРОВАНИЯ
import logging

logger = logging.getLogger('django')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style' : '{',
    # 'datefmt': "%d.%m.%Y / %H-%M-%S /",

    'filters': {
        'debug_true': {'()': 'django.utils.log.RequireDebugTrue',},
        'debug_false': {'()': 'django.utils.log.RequireDebugFalse',},
    },

    'formatters': {
        'simple': {'format': '%(asctime)s %(levelname)s %(message)s',
                   'datefmt': "%d.%m.%Y %H-%M-%S"},
        'simple_warning':{'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s',
                   'datefmt': "%d.%m.%Y %H-%M-%S"},
        'simple_error':{'format': '%(asctime)s %(levelname)s %(message)s %(exc_info)s',
                   'datefmt': "%d.%m.%Y %H-%M-%S"},
        'general':{ 'format': '%(asctime)s = %(levelname)s = %(module)s = %(message)s',
                   'datefmt': "%d.%m.%Y : %H-%M-%S"},
        'errors':{'format': '%(asctime)s = %(levelname)s = %(message)s = %(pathname)s = %(exc_info)s',
                  'datefmt': "%d.%m.%Y %H-%M-%S"},
        'email':{'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s',
                  'datefmt': "%d.%m.%Y %H-%M-%S"},
        'security':{'format': '%(asctime)s %(levelname)s %(module)s %(message)s',
                  'datefmt': "%d.%m.%Y %H-%M-%S"},
    },

    'handlers': {
        'console': { #1
            'level': 'DEBUG',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'},
        'console_warning': { #2
            'level': 'WARNING',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_warning' },
        'console_error': { #3
            'level': 'ERROR',
            'filters': ['debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_error'},
        'general': { #4
            'level': 'INFO',
            'filters': ['debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'general',
            'filename':'logs/general.log'},
        'errors': { #5
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'errors',
            'filename':'logs/errors.log'},
        'security': { #6
            'level': 'DEBUG', # может быть так же значение 'INFO', или даже 'WARNING'
            'class': 'logging.FileHandler',
            'formatter': 'security',
            'filename': 'logs/security.log'},  ###
        'mail_admins': { #7
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'email',
            'filters': ['debug_false'], # 'include_html': False,
        },###
    },
    'loggers': {
        'django': {
            'handlers': ['console','console_warning','console_error','general'],'propagate': True,},
        'django.request': {
            'handlers': ['mail_admins','errors'],'propagate': True,},
        'django.server': {
            'handlers': ['mail_admins','errors'],'propagate': True,},
        'django.template': {
            'handlers': ['errors'],'propagate': True, },
        'django.db_backends': {
            'handlers': ['errors'],'propagate': True, },
        'django.security': {
            'handlers': ['security'],'propagate': True, },
    }
}

ADMINS = [
    ('Admin', EMAIL_HOST_USER ),
]



# ДЛЯ ЛОКАЛИЗАЦИИ
USE_I18N = True
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en-us','English'),
    ('ru','Русский'),
]

