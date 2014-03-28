from sqlalchemy import func
from flask import Blueprint, request, render_template, g


mod = Blueprint('about', __name__, url_prefix='/about')

@mod.before_request
def before_request():
    g.page_type = mod.name
    
    g.color = "#d67ab0"

@mod.route('/')
def about():
    return render_template("about/pecbrasil.html", page = "pecbrasil")
    
#   Pagina-Como-Funciona---PEC-Brasil  - OK
#        URL: /about/regras
#        HTML: html/about/regras.html
#        SERVICO: Nenhum (apenas conteudo estatico)
@mod.route('/regras/')
def regras():
    return render_template("about/regras.html")