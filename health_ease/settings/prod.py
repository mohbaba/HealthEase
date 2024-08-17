from .settings import *


DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*.fly.dev', 'health-ease-icy-violet-612.fly.dev']
CSRF_TRUSTED_ORIGINS = ['https://health-ease.fly.dev', 'https://health-ease-icy-violet-612.fly.dev']

DATABASES = {
    # 'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
