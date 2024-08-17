from .settings import *

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
