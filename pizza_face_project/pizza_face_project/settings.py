"""
Django settings for pizza_face_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import dj_database_url # for heroku use
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm=%n89b2y4nsk_iyhwh&pm@v#%&ydc6mdw7+u-jhtjhj=zqz%i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pizza_ml.apps.PizzaMlConfig',
    'rest_framework', # creates api's
    'corsheaders', # allows cross site api
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # allows permissions cross site api
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


CORS_ORIGIN_ALLOW_ALL = True # allows permissions cross site api


ROOT_URLCONF = 'pizza_face_project.urls'

WSGI_APPLICATION = 'pizza_face_project.wsgi.application'

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
    )
    

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DB settings for Heroku
DATABASES = {  
    'default': {      
        'ENGINE': 'django.db.backends.postgresql_psycopg2',     
        'NAME': 'pizzaml',                           
        'USER': 'pizzafac',       
        'PASSWORD': 'password',       
        'HOST': 'localhost',        
        'PORT': '',   
    }
}

DATABASE_URL = postgres://dbecegbybpremj:Yz8bDwrQ5O-Th_TTzm9eFJqslF@ec2-54-228-192-254.eu-west-1.compute.amazonaws.com:5432/dbjjt9o5mpd192

# Below is adivice for heroku from
# https://devcenter.heroku.com/articles/django-app-configuration
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Redirects non logged in users
LOGIN_URL = '/login/'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage' # adviced by Heroku

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


PASSWORD_HASHERS = (
'django.contrib.auth.hashers.PBKDF2PasswordHasher',
'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

#REST_FRAMEWORK = {
#    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'rest_framework.authentication.BasicAuthentication',
#        'rest_framework.authentication.SessionAuthentication',
#    ),
#    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
#    'PAGINATE_BY': 10
#}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        )
}