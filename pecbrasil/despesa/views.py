from sqlalchemy import func, distinct
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for


from pecbrasil import db
from pecbrasil.politica.models import Candidatura, Pontuacao
from pecbrasil.utils import exist_or_404, gzip_data, cached_query
from pecbrasil.politica.services import PoliticaServices

mod = Blueprint('despesa', __name__, url_prefix='/despesa')
politicaServices = PoliticaServices()   

@mod.route('/tipo/')
@mod.route('/tipo/<nome>')
def tipo(nome=None):
    if nome is not None:
        return render_template("despesa/despesa.html",nome=nome)
    else:
        return None

@mod.route('/boxdespesa')
@mod.route('/boxdespesa/<nome>')
def boxdespesa(nome=None):
    despesas=politicaServices.despesaByTipo(nome) 
    if despesas is not None:
        return render_template("despesa/boxdespesa.html",despesas=despesas,nome=nome)
    else:
        return None

@mod.route('/treemap/')
@mod.route('/treemap/<partido>')
@mod.route('/treemap/<partido>/<politicoid>')
def treemap(partido=None,politicoid=None): 
    if partido is  None:
        return render_template("despesa/treemap.html" )
    else:
        if partido == 'all':
            return render_template("despesa/treemap.html",politicoid=politicoid )
        else:
            return render_template("despesa/treemap.html",partido=partido,politicoid=politicoid )


@mod.route('/stacked/')
@mod.route('/stacked/<partido>')
@mod.route('/stacked/<partido>/<politicoid>')
def stacked(partido=None,politicoid=None): 
    if partido is  None:
        return render_template("despesa/stacked.html" )
    else:
        if partido == 'all':
            return render_template("despesa/stacked.html",politicoid=politicoid )
        else:
            return render_template("despesa/stacked.html",partido=partido,politicoid=politicoid )
