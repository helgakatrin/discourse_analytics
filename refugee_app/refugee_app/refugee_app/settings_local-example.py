KEYWORDS =  ['word1', 'word2']

# Get your API key here: https://developers.facebook.com/tools/explorer/
FB_API_KEY = "your-facebook-api-key"

# Remote postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5433,
    }
}