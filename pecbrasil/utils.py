import cStringIO, gzip, pickle, re
from re import sub
from decimal import Decimal
from werkzeug.datastructures import CallbackDict
from jinja2 import Markup
from flask import abort, current_app
from datetime import datetime, date, timedelta
from math import ceil
from uuid import uuid4
from redis import Redis
import string
from flask.sessions import SessionInterface, SessionMixin

############################################################
# ----------------------------------------------------------
# Utility methods for entire site
# 
############################################################

''' A Mixin class for retrieving public fields from a model
    and serializing them to a json-compatible object'''
class AutoSerialize(object):
    __public__ = None

    def serialize(self, exclude=(), extra=()):
        "Returns model's PUBLIC data for jsonify"
        data = {}
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        allowed = []
        
        for k, field in  keys:
            if public and k not in public:                
                continue
            if k in exclude:
                continue
            value = None
            
            if isinstance(field.value, Decimal):
                value=float(field.value)        
            elif isinstance(field.value,unicode) or \
                                    isinstance(field.value,float) or \
                                    isinstance(field.value,int) or \
                                    isinstance(field.value,str) or \
                                    isinstance(field.value,long):
                value = self._serialize(field.value)
            else: 
                value = self._serialize(field.value)
            
            if value is not None:
                data[k] = value
        
        return data
    
    def serialize2(self):
        
        data = self.__dict__
        public = self.__public__
        allowed = []
        
        for key, value in data.iteritems():
            
            if isinstance(value,unicode) or \
                                    isinstance(value,float) or \
                                    isinstance(value,int) or \
                                    isinstance(value,str) or \
                                    isinstance(value,long):
                allowed.append((key,value))
        
        data = dict(allowed)
        
        return data


    @classmethod
    def _serialize(cls, value, follow_fk=False):
        
        if type(value) in (datetime, date):
            ret = value.isoformat()
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AutoSerialize in value.__class__.__bases__:
            ret = value.serialize()
        else:
            ret = value

        return ret

''' A helper class for dealing with injecting times into the page using moment.js'''
class Momentjs:
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>" % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
        
class formatter:
    def __init__(self, text):
        self.text = text
        
    def render(self, type, lang):
        if isinstance(self.text,unicode) or isinstance(self.text,str):
            format = "text"
        else:
            format = "number"
            
        return Markup("<script>\ndocument.write(pecbrasil.format.%s(\"%s\",\"%s\",\"%s\"))\n</script>" % (format, self.text, type, str(lang)))

''' A helper funciton for stripping out html tags for showing snippets of user submitted content'''
def strip_html(s):
    return sub('<[^<]+?>', '', s)

def jinja_split(s, char):
    return s.split(char)

''' A helper function for retrieving a specific item from the given model that
    will raise a 404 error if not found in the DB'''
def exist_or_404(Model, id):
    item = Model.query.get(id)
    if item:
        return item
    abort(404, 'Entry not found in %s with id: %s' % (Model.__tablename__, id))

''' Helper function to gzip JSON data (used in data API views)'''
def gzip_data(json):
    # GZip all requests for lighter bandwidth footprint
    gzip_buffer = cStringIO.StringIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
    gzip_file.write(json)
    gzip_file.close()
    return gzip_buffer.getvalue()

''' Get/Sets a given ID in the cache. If data is not supplied, 
    used as getter'''
def cached_query(id, data=None):
    c = current_app.config.get('REDIS')
    if data is None:
        return c.get(id)
    return c.set(id, data)

''' Given a "year" string from URL, turn this into an array of years 
    as integers'''
def parse_years(year_str):
    year_str = str(year_str)
    if "-" in year_str:
        # we allow a range of years w/ or w/o interval (using '.' as sep)
        year_start, year_end = year_str.split("-")
        if "." in year_end:
            year_end, year_interval = year_end.split(".")
        else:
            year_interval = "1"
        years = range(int(year_start), int(year_end)+1, int(year_interval))
    else:
        # we allow a set of years (with '+' between)
        years = [int(y) for y in year_str.split("+")]
    return years
    
''' Titlecase Function '''
def title_case(string):
    exceptions = ['A', 'An', 'And', 'As', 'At', 'But', 'By', 'For', 'From', 'If', \
              'In', 'Into', 'Near', 'Nor', 'Of', 'On', 'Onto', 'Or', 'That', \
              'The', 'To', 'With', 'Via', 'Vs', 'Vs.', \
              'Um', 'Uma', 'E', 'Como', 'Em', 'No', 'Na', 'Mas', 'Por', \
              'Para', 'Pelo', 'Pela', 'De', 'Do', 'Da', 'Se', 'Perto', 'Nem', \
              'Ou', 'Que', 'O', 'A', 'Com']
    words = re.split(" ",string)
    final = [words[0].capitalize()]
    for word in words[1:]:
        if word in exceptions or word.capitalize() in exceptions:
            final.append(word.lower())
        else:
            final.append(word.capitalize())
    return " ".join(final)

def clean_varrequest(variavel,padrao=None):
    if variavel is None or variavel =="None" or variavel.upper() =="ALL":
        return padrao
    return variavel

from flask.ext.mail import Message

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

''' We are using a custom class for storing sessions on the serverside instead
    of clientside for persistance/security reasons. See the following:
    http://flask.pocoo.org/snippets/75/ '''
class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)

"""
Module that provides a class that filters profanities

f = ProfanitiesFilter(['bad', 'un\w+'], replacements="-")
example = "I am doing bad ungood badlike things."

print f.clean(example)
# Returns "I am doing --- ------ badlike things."

f.inside_words = True
print f.clean(example)
# Returns "I am doing --- ------ ---like things."

f.complete = False
print f.clean(example)
# Returns "I am doing b-d u----d b-dlike things."

"""

import random
import re

class ProfanitiesFilter(object):
    def __init__(self, filterlist, ignore_case=True, replacements="$@%-?!",
                 complete=True, inside_words=False):
        """
Inits the profanity filter.

filterlist -- a list of regular expressions that
matches words that are forbidden
ignore_case -- ignore capitalization
replacements -- string with characters to replace the forbidden word
complete -- completely remove the word or keep the first and last char?
inside_words -- search inside other words?

"""

        self.badwords = filterlist
        self.ignore_case = ignore_case
        self.replacements = replacements
        self.complete = complete
        self.inside_words = inside_words

    def _make_clean_word(self, length):
        """
Generates a random replacement string of a given length
using the chars in self.replacements.

"""
        return ''.join([random.choice(self.replacements) for i in
                  range(length)])

    def __replacer(self, match):
        value = match.group()
        if self.complete:
            return self._make_clean_word(len(value))
        else:
            return value[0]+self._make_clean_word(len(value)-2)+value[-1]

    def clean(self, text):
        """Cleans a string from profanity."""

        regexp_insidewords = {
            True: r'(%s)',
            False: r'\b(%s)\b',
            }

        regexp = (regexp_insidewords[self.inside_words] %
                  '|'.join(self.badwords))

        r = re.compile(regexp, re.IGNORECASE if self.ignore_case else 0)

        return r.sub(self.__replacer, text)
    
    
''' Send email to users
recipients=["dataviva@googlegroups.com","datavivaweb@gmail.com"]
title="Hello"
message="Invite friends: {0}".format(name)
'''
def send_mail(title, recipients,message):
    from pecbrasil import mail
    msg = Message(title,sender="Politica Esporte Clube <contato@politicaesporteclube.com>",recipients=recipients)
    msg.body = message
    msg.html = msg.body
    mail.send(msg)