import os
from pathlib import Path
from django.contrib.messages import constants as messages
from decouple import config, Csv


MESSAGE_TAGS = {
        messages.DEBUG: 'bg-secondary',
        messages.INFO: 'bg-info',
        messages.SUCCESS: 'bg-success',
        messages.WARNING: 'bg-warning',
        messages.ERROR: 'bg-danger',
 }


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'widget_tweaks',
    'django_filters',
    'debug_toolbar',
    'django_cleanup.apps.CleanupConfig',
    'multiselectfield',
    'django_htmx',
    'django_select2',
    'migration_fixer',

    #apps SIMO
    'estoque.apps.EstoqueConfig',
    'requisicao.apps.RequisicaoConfig',
    'obras.apps.ObrasConfig',
    'servicos.apps.ServicosConfig',
    'funcionarios.apps.FuncionariosConfig',
    'clientes.apps.ClientesConfig',
    'usuarios.apps.UsuariosConfig',
    'recibos.apps.RecibosConfig',
    'fornecedores.apps.FornecedoresConfig',
    'financeiro.apps.FinanceiroConfig',
    'dashboard.apps.DashboardConfig',
    'tarefas.apps.TarefasConfig',
    'faturamento',
    'engenharia',
    'estoque_v2',
    

]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'simo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'templates').replace('\\','/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                

            ],
            'libraries': {
                'my_tags': 'simo.templatetags.my_filter_tags',
            },
        },
    },
]

WSGI_APPLICATION = 'simo.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD' : config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}


# CACHE configurations
CACHES = {
    'default': {
        'BACKEND': config('BACKEND'),
        'LOCATION': config('LOCATION'),
        'TIMEOUT': 3600  # 1 hora
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
]

# Password validation
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
LANGUAGE_CODE = 'pt-BR'
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
TIME_ZONE = 'America/Sao_Paulo'
DATE_FORMAT = 'd/m/Y'

DECIMAL_SEPARATOR = ','
USE_THOUSAND_SEPARATOR = True

USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
MEDIA_URL = '/media/'


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')


if DEBUG:
	STATICFILES_DIRS = [
		os.path.join(PROJECT_ROOT, 'static')
       ]
else:
	STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
       



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#CONFIGURAÃ‡Ã•ES DE AUTENTICAÃ‡ÃƒO
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

TEMPLATE_DEBUG = DEBUG
