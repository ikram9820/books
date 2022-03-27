from .common import *


DEBUG = True
SECRET_KEY = 'django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k**r'


STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'books',
        'PASSWORD':'root',
        'USER':'root',
        'HOST':'localhost',
        'PORT': '3306'

        }
}
