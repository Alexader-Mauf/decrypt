import os
"""
Django settings for decrypt project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y%dhwlx69v2*man8%zjt5&3de*vb_x3-g3e+8ut_d%es=0n9o5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_L10N = True

USE_TZ = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third Party
    'django_seed',
    'rest_framework',
    'django_filters',
    'pipeline',
    #Own
    'core',
    'key',
    'keyform',
    'bank',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = (
   'django.middleware.gzip.GZipMiddleware',
   'pipeline.middleware.MinifyHTMLMiddleware',
)


ROOT_URLCONF = 'decrypt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'decrypt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ATOMIC_REQUESTS' : True,
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'banking',
        'USER': 'root',
        'PASSWORD': 'yfKWPwjUZnie[yeZGKPA',
        'HOST': '127.0.0.1',
        'PORT': '3306',
   }
}
# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'CET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,  'key/static/')

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)


PIPELINE = {
    'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
    'keyform': {
        'source_filenames': (
            'css/bootstrap.css',
            'css/cover.css',
            'css/product.css',
        ),
        'output_filename': 'css/keyform.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
    #'stylesheetsbanking':{
    #    'source_filenames':(
    #        'device-mockups/device-mockups.min.css',
    #        'css/bootstrap.css',
    #        'vendor/simple-line-icons/css/simple-line-icons.css',
    #        'vendor/fontawesome-freecss/all.min.css',
    #        'css/new-age.css',
    #        'device-mockups/device-mockups.min.css',
    #    ),
    #    'output_filename':'css/stylesheetsbanking.css',
    #}
},
    'JAVASCRIPT': {
        'jscripts': {
            'source_filenames': (
              'js/jquery-3.5.1.min.js',
              'js/read_write_data.js',
            ),
            'output_filename': 'js/jscripts.js',
        },
        #'bankingjscripts':{
        #    'source_filenames':(
        #        'vendor/jquery/jquery.min.js',
        #        'vendor/bootstrap/js/bootstrap.bundle.min.js',
        #        'vendor/jquery-easing/jquery.easing.min.js',
        #        'templateforbankkingapp/js/new-age.min.js',
        #    ),
        #    'output_filename':'js/bankingjscripts.js'
        #}
    },


    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor'}





