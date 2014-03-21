from datetime import datetime
from flask import Blueprint, render_template, g, request, current_app, session, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.babel import gettext
from pecbrasil.ask.forms import AskForm
import time

mod = Blueprint('general', __name__, url_prefix='/')

from pecbrasil import app, db, babel, __latest_year__
from pecbrasil.general.forms import AccessForm
from pecbrasil.politica.services import PoliticaServices
politicaServices = PoliticaServices()
###############################
# General functions for ALL views
# ---------------------------
@app.before_request
def before_request():
    
    g.timing = []
    g.timing.append(time.time())
    g.color = "#af1f24"
    g.page_type = mod.name
    g.latest_year = {}
    for dataset in __latest_year__:
        g.latest_year[dataset] = __latest_year__[dataset]
    
    t1 = time.time()
    
    # Check if the user has access (temp log in for development purposes)
    if 'has_access' not in session:
        session['has_access'] = False
    
    # test if the user has access!
    if not session['has_access'] and request.endpoint and request.endpoint != "static":
        session['has_access'] = True
 
    if 'rodada_atual' not in session:
        session['rodada_atual'] = politicaServices.rodadaAtual()
       
#        if request.endpoint == "general.home":
#            form = AccessForm()
            
#            if "pw" in request.form:
                
#                if request.form["pw"] == "parabens":
#                    session['has_access'] = True
                    
#                else:
#                    return render_template("general/access.html", form=form)
#            else:
#                return render_template("general/access.html", form=form)
#        else:
#            return redirect(url_for("general.home"))
            
    # Save variable in session so we can determine if this is the user's
    # first time on the site
    if 'first_time' in session:
        session['first_time'] = False
    else:
        session['first_time'] = True
        # flash("I've noticed it's your first time on the site. Welcome!")
    
    # Check if the user is logged in, if so give the global object
    # a reference to the user from DB
    g.user = current_user
    
    if g.user.is_authenticated() and request.endpoint != 'static':        
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
    
    # Set the locale to either 'pt' or 'en' on the global object
    if request.endpoint != 'static':
        g.locale = get_locale()
    
    t2 = time.time()
    g.timing.append("Global Before Request: {0:.4f}s".format(t2-t1))

@babel.localeselector
def get_locale(lang=None):
    supported_langs = current_app.config['LANGUAGES'].keys()
    new_lang = request.accept_languages.best_match(supported_langs, "pt")
    # user = getattr(g, 'user', None)
    user = current_user
    if lang:
        if lang in supported_langs:
            new_lang = lang
        if user.is_authenticated():
            # set users preferred lang
            user.language = new_lang
            db.session.add(user)
            db.session.commit()
        else:
            session['locale'] = new_lang
    else:
        current_locale = getattr(g, 'locale', None)
        # return new_lang
        if current_locale:
            new_lang = current_locale
        elif user.is_authenticated():
            user_preferred_lang = getattr(user, 'language', None)
            if user_preferred_lang and user_preferred_lang in supported_langs:
                new_lang = user_preferred_lang
            else:
                # set users preferred lang
                user.language = new_lang
                db.session.add(user)
                db.session.commit()
        elif 'locale' in session:
            new_lang = session['locale']
        else:
            session['locale'] = new_lang
    
    return new_lang

@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None:
        return user.timezone

###############################
# General views 
# ---------------------------
@app.after_request
def after_request(response):
    overall = (time.time()-g.timing[0])
    g.timing[0] = "Overall: {0:.4f}s".format(overall)
    # raise Exception(g.timing)
    # if overall > 10:
        # raise Exception(g.timing)
    return response

#    Pagina-Principal---PEC-Brasil(Alterado)
#        URL: /
#        HTML: html/home.html
#        SERVICOS: top3Time
@mod.route('/', methods=['GET', 'POST'])
def home():
    g.page_type = "home"
    rodada_atual = db.session.merge(session['rodada_atual'])
    if g.user is not None and g.user.is_authenticated() \
        and ('user_time' not in session or session['user_time']) :
        timeRetorno = politicaServices.meuTime(g.user.id) 
        if timeRetorno is None:
            return   redirect(url_for('politica.criarPartido'))
    
    rodadaAtual= politicaServices.rodadaAtual()
    top3Time= politicaServices.top3Time()
    topPol= politicaServices.topPoliticosRodada(None,10)
    num_lines=0
    primeiro=None
    segundo=None
    terceiro=None
    for line in top3Time:       
        num_lines += 1
        if num_lines == 1:
            primeiro = line
        elif num_lines == 2:
            segundo = line
        else:
            terceiro = line
    form=AskForm()
    return render_template("home.html",form=form,primeiroTime=primeiro,segundoTime=segundo,
                   terceiroTime=terceiro,topPol=topPol,rodada_atual=rodada_atual)

@mod.route('access/')
@mod.route('access/logout/')
def access():
    session['has_access'] = False
    return redirect(url_for('general.home'))

###############################
# Set language views 
# ---------------------------
@mod.route('set_lang/<lang>/')
def set_lang(lang):
    g.locale = get_locale(lang)
    return redirect(request.args.get('next') or \
               request.referrer or \
               url_for('general.home'))

###############################
# 404 view
# ---------------------------
@app.errorhandler(404)
def page_not_found(e):
    g.page_type = "error404"

    sabrina = {}
    sabrina["outfit"] = "lab"
    sabrina["face"] = "scared"
    sabrina["hat"] = None
    
    return render_template('general/404.html', 
        error = e, sabrina = sabrina), 404