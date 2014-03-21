import os
from os import environ
import datetime
# general flask library
from flask import Flask
# flask-sqlalchemy connector for database queries
from flask.ext.sqlalchemy import SQLAlchemy
# flask-login for managing users
from flask.ext.login import LoginManager
# flask-babel for handling L18n and L10n
from flask.ext.babel import Babel
# for new filters, redis sessions
from utils import Momentjs, formatter, strip_html, jinja_split, RedisSessionInterface
from flask.ext.mail import Mail

''' Base directory of where the site is held '''
pecbrasildir = os.path.abspath(os.path.dirname(__file__))

# Initialize app
app = Flask(__name__, template_folder=os.path.join(pecbrasildir, 'html'))

# Load default configuration from config.py
app.config.from_object('config')

# DB connection object
db = SQLAlchemy(app)

mail = Mail(app)

# Set session store as server side (Redis)
app.session_interface = RedisSessionInterface()

#DEBUG
app.debug = True 

# Global Latest Year Variables
__latest_year__ = {"secex": 2011, "rais": 2010}

# login manager for user management
lm = LoginManager()
lm.setup_app(app)

# babel configuration for lang support
babel = Babel(app)

def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.format_datetime(value, format)

def _jinja2_filter_datetime(date, fmt='%c'):
    # check whether the value is a datetime object
    if not isinstance(date, (datetime.date, datetime.datetime)):
        try:
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception, e:
            return date
    return date.strftime(fmt)

# add a few extra template filters to jinja
app.jinja_env.globals['momentjs'] = Momentjs
app.jinja_env.globals['format'] = formatter
app.jinja_env.filters['strip_html'] = strip_html
app.jinja_env.filters['split'] = jinja_split
app.jinja_env.filters['datetime'] = _jinja2_filter_datetime

# Load the modules for each different section of the site
''' data API view/models '''
from pecbrasil.attrs.views import mod as attrs_module
from pecbrasil.liga.views import mod as liga_module
from pecbrasil.politica.views import mod as politica_module
from pecbrasil.general.views import mod as general_module
from pecbrasil.admin.views import mod as admin_module
from pecbrasil.account.views import mod as account_module
from pecbrasil.ask.views import mod as ask_module
from pecbrasil.about.views import mod as about_module
from pecbrasil.grafico.views import mod as grafico_module
from pecbrasil.politico.views import mod as politico_module
from pecbrasil.despesa.views import mod as despesa_module
from pecbrasil.pontos.views import mod as pontos_module
from pecbrasil.proposicao.views import mod as proposicao_module
from pecbrasil.orgao.views import mod as orgao_module
from pecbrasil.comunicado.views import mod as comunicado_module
from pecbrasil.rodada.views import mod as rodada_module

''' Register these modules as blueprints '''
app.register_blueprint(attrs_module)
app.register_blueprint(general_module)
app.register_blueprint(admin_module)
app.register_blueprint(account_module)
app.register_blueprint(ask_module)
app.register_blueprint(about_module)
app.register_blueprint(politica_module)
app.register_blueprint(politico_module)
app.register_blueprint(grafico_module)
app.register_blueprint(despesa_module)
app.register_blueprint(pontos_module)
app.register_blueprint(liga_module)
app.register_blueprint(proposicao_module)
app.register_blueprint(orgao_module)
app.register_blueprint(comunicado_module)
app.register_blueprint(rodada_module)
