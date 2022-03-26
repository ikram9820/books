from .common import *


DEBUG = True
SECRET_KEY = 'django-insecure-6j2@8g)ygvsiuvnh1w8cs&o)k*o!l_t5j5jskw0ecs($*1s1*r'

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
