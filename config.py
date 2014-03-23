# -*- coding: utf-8 -*-
import os
from werkzeug.contrib.cache import RedisCache

'''
    Used for finding environment variables through configuration
    if a default is not given, the site will raise an exception
'''
def get_env_variable(var_name, default=-1):
    try:
        return os.environ[var_name]
    except KeyError:
        if default != -1:
            return default
        error_msg = "Set the %s os.environment variable" % var_name
        raise Exception(error_msg)

''' Base directory of where the site is held '''
basedir = os.path.abspath(os.path.dirname(__file__))

''' CSRF (cross site forgery) for signing POST requests to server '''
CSRF_EN = True

''' Secret key should be set in environment var '''
SECRET_KEY = get_env_variable("PEC_SECRET_KEY", "default-pecbrasil.mg-secr3t")

''' Default debugging to True '''
DEBUG = True
SQLALCHEMY_ECHO = True

''' 
    Details for connecting to the database, credentials set as environment
    variables.
'''
SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(
    get_env_variable("PEC_DB_USER", "sisfocus_pec"), 
    get_env_variable("PEC_DB_PW", "pec2014"), 
    get_env_variable("PEC_DB_HOST", "198.50.106.250"),
    get_env_variable("PEC_DB_NAME", "sisfocus_pec"))

''' If user prefers to connect via socket set env var '''
if "PEC_DB_SOCKET" in os.environ:
    SQLALCHEMY_DATABASE_URI += "?unix_socket=" + get_env_variable("PEC_DB_SOCKET","")

''' If an env var for production is set turn off all debugging support '''
if "PEC_PRODUCTION" in os.environ:
    SQLALCHEMY_ECHO = False
    DEBUG = False

''' Available languages '''
LANGUAGES = {
    'en': 'English',
    'pt': 'Português',
    'es': 'Espanhol'
}

''' For full text search '''
WHOOSH_BASE = os.path.join(basedir, 'search.db')

''' 
    Setup redis caching connection to be used throughout the site. Credentials
    are set in their respective env vars.
'''
REDIS = RedisCache(host=get_env_variable("PEC_REDIS_HOST", "localhost"), 
         port=get_env_variable("PEC_REDIS_PORT", 6379), 
         password=get_env_variable("PEC_REDIS_PW", None), default_timeout=2591999)

'''
    Oauth tokens set in environment variables from their respecive sources
'''
GOOGLE_OAUTH_ID = get_env_variable("PEC_OAUTH_GOOGLE_ID","853706737689.apps.googleusercontent.com")
GOOGLE_OAUTH_SECRET = get_env_variable("PEC_OAUTH_GOOGLE_SECRET","4yao9LxFZamSlKhaDfJqWThX")
TWITTER_OAUTH_ID = get_env_variable("PEC_OAUTH_TWITTER_ID","tGeRUWsa2DVtTZ0GpLRcsg")
TWITTER_OAUTH_SECRET = get_env_variable("PEC_OAUTH_TWITTER_SECRET","AyGK7At3XBClpmhPCqc22GcQwlL0Ajz0KKhYHpwCcY")
FACEBOOK_OAUTH_ID = get_env_variable("PEC_OAUTH_FACEBOOK_ID","208773702609294")
FACEBOOK_OAUTH_SECRET = get_env_variable("PEC_OAUTH_FACEBOOK_SECRET","733769c31c23eecf2e35e1c06915e89b")

# email server GMAIL
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'pecbrcontato@gmail.com'
MAIL_PASSWORD = 'pecBR2014'

# email server iweb
MAIL_SERVER = 'server.croquiteca.com.br'
MAIL_USERNAME = 'contato@politicaesporteclube.com'

# email server LIVE - OUTLOOK
#MAIL_SERVER = 'smtp.live.com'
#MAIL_PORT = 587
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'contato@politicaesporteclube.com'
#MAIL_PASSWORD = 'pecBR123'




# administrator list
ADMINS = ['your-gmail-username@gmail.com']
