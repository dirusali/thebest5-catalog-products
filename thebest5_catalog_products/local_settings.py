ALLOWED_HOSTS=['*']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "catalog",
        'USER': "best5",
        'PASSWORD': "best5",
        'HOST': "127.0.0.1",
        'PORT': 5432
    }
}
