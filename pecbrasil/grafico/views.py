from sqlalchemy import func, distinct
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for


from pecbrasil import db
from pecbrasil.politica.models import Candidatura, Pontuacao
from pecbrasil.utils import exist_or_404, gzip_data, cached_query

mod = Blueprint('grafico', __name__, url_prefix='/grafico')


@mod.route('/treemap/')
@mod.route('/treemap/<partido>')
@mod.route('/treemap/<partido>/<politicoid>')
@mod.route('/treemap/<partido>/<politicoid>/')
def treemap(partido=None,politicoid=None): 
    if partido is  None:
        return render_template("grafico/treemapPartido.html" )
    else:
        if partido == 'all':
            return render_template("grafico/treemap.html",politicoid=politicoid )
        else:
            return render_template("grafico/treemap.html",partido=partido,politicoid=politicoid )

@mod.route('/stacked/')
@mod.route('/stacked/<partido>')
@mod.route('/stacked/<partido>/')
@mod.route('/stacked/<partido>/<politicoid>')
@mod.route('/stacked/<partido>/<politicoid>/')
def stacked(partido=None,politicoid=None):    
    if partido is  None:
        return render_template("grafico/stackedPartido.html" )
    else:
        if partido == 'all':
            return render_template("grafico/stacked.html",politicoid=politicoid )
        else:
            return render_template("grafico/stacked.html",partido=partido,politicoid=politicoid )

@mod.route('/compare/')
def compare():    
    return render_template("grafico/compare.html" )

@mod.route('/geomap/')
def geomap():    
    return render_template("grafico/geomap.html" )

@mod.route('/network/')
def network():    
    return render_template("grafico/network.html" )

@mod.route('/bubbles/')
@mod.route('/bubbles/<partido>')
@mod.route('/bubbles/<partido>/')
@mod.route('/bubbles/<partido>/<politicoid>')
@mod.route('/bubbles/<partido>/<politicoid>/')
def bubbles(partido=None,politicoid=None):    
    if partido is  None:
        return render_template("grafico/bubblesPartido.html" )
    else:
        if partido == 'all':
            return render_template("grafico/bubbles.html",politicoid=politicoid )
        else:
            return render_template("grafico/bubbles.html",partido=partido,politicoid=politicoid )


@mod.route('/bubblesvotacoes/')
@mod.route('/bubblesvotacoes/<proposicao_id>')
@mod.route('/bubblesvotacoes/<proposicao_id>/')
@mod.route('/bubblesvotacoes/<proposicao_id>/<politicoid>')
@mod.route('/bubblesvotacoes/<proposicao_id>/<politicoid>/')
def bubblesvotacoes(proposicao_id=None,politicoid=None):    
    if proposicao_id is  None:
        return None
    else:
        if politicoid == 'all' or politicoid is None:
            return render_template("grafico/bubblesvotacoes.html",proposicao_id=proposicao_id )
        else:
            return render_template("grafico/bubblesvotacoes.html",proposicao_id=proposicao_id,politicoid=politicoid )


@mod.route('/rings/')
def rings():    
    return render_template("grafico/rings.html" )

@mod.route('/scatter/')
def scatter():    
    return render_template("grafico/scatter.html" )


@mod.route('/selecaostacked/<selecao>')
@mod.route('/selecaostacked/<selecao>/<liga>')
@mod.route('/selecaostacked/<selecao>/<liga>/')
def selecaostacked(selecao=None,liga=None):    
    if selecao is not  None:
        return render_template("grafico/selecao.html",selecao=selecao ,liga=liga)
    

@mod.route('/mapasvg/')
def mapasvg():    
    AM=request.args.get('AM')
    
    return render_template("grafico/mapEstadosBrasilSVG.html",AM=AM )
