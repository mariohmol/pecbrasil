from sqlalchemy import func, distinct
from flask import Blueprint, request, jsonify, abort, g

from pecbrasil import db
from pecbrasil.politica.models import Candidatura,CandidaturaTotal, Pontuacao,Partido,PartidoTotal,Time,RodadaPontos,TimeCandidato 
from pecbrasil.politica.models import DespesaTipo,Rodada,ProcessoCandidato,DespesaCandidato
from pecbrasil.liga.models import LigaPontos,Liga,LigaJogador

from pecbrasil.proposicao.models import VotacaoCandidato,Proposicao,TimeVotacao
from pecbrasil.orgao.models import Orgao,OrgaoCandidato
from pecbrasil.utils import exist_or_404, gzip_data, cached_query
from pecbrasil.politica.services import PoliticaServices
from pecbrasil.account.models import User

try:
    # this is how you would normally import
    from flask.ext.cors import cross_origin
except:
    # support local usage without installed package
    from flask_cors import cross_origin



from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


mod = Blueprint('attrs', __name__, url_prefix='/attrs')
politicaServices = PoliticaServices()   
cacheFlag=False

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

@mod.before_request
def before_request():
    limit = request.args.get('limit')  
    offset = request.args.get('offset')  
    cache_id = request.path + g.locale + str(limit) + str(offset)

    # first lets test if this query is cached
    cached_q = cached_query(cache_id)
    if cached_q and cacheFlag and request.method != 'OPTIONS' and request.method != 'POST': # and request.is_xhr and limit is None and offset is None:
        return cached_q

@mod.after_request
def after_request(response):
    limit = request.args.get('limit')  
    offset = request.args.get('offset') 
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Credentials'] = "true"
    response.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With,Content-Type, Accept"
    # if response.status_code != 302:
    if response.status_code != 302: # and request.is_xhr
        
        cache_id = request.path + g.locale + str(limit) + str(offset)
        # test if this query was cached, if not add it
        cached_q = cached_query(cache_id)
        if cached_q is None and cacheFlag and request.method != 'OPTIONS' and request.method != 'POST':
            response.data = gzip_data(response.data)
            cached_query(cache_id, response.data)
       
        #if request.method != 'OPTIONS' and request.method != 'POST':
        #    response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    
    return response


#    return jsonify(ret)

@mod.route('/candidatura/', methods=['GET', 'POST'])
@mod.route('/candidatura/<candidatura_id>', methods=['GET', 'POST'])
@mod.route('/candidatura/<candidatura_id>/', methods=['GET', 'POST'])
@mod.route('/candidatura/<candidatura_id>/<partido_sigla>', methods=['GET', 'POST'])
@mod.route('/candidatura/<candidatura_id>/<partido_sigla>/', methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_candidatura(candidatura_id=None,partido_sigla=None):

    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 100)    

    ret = None
    if candidatura_id == 'all' and partido_sigla is not None and partido_sigla <> 'all':
        ret = politicaServices.candidaturaByPartido(partido_sigla,limit=limit) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = Candidatura.query.limit(limit).offset(offset).all()
    elif candidatura_id is not None and candidatura_id<>'all':
        ret = Candidatura.query.filter_by(id=candidatura_id).limit(limit).offset(offset).all()
    else:
        ret = Candidatura.query.limit(limit).offset(offset).all()
       
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"candidaturas":items})
    else:
        return ''

@mod.route('/candidaturatotal/', methods=['GET', 'POST'])
@mod.route('/candidaturatotal/<candidatura_id>', methods=['GET', 'POST'])
@mod.route('/candidaturatotal/<candidatura_id>/', methods=['GET', 'POST'])
@mod.route('/candidaturatotal/<candidatura_id>/<partido_sigla>', methods=['GET', 'POST'])
@mod.route('/candidaturatotal/<candidatura_id>/<partido_sigla>/', methods=['GET', 'POST'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_candidaturatotal(candidatura_id=None,partido_sigla=None):

    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 10000)    

    ret = None
    if candidatura_id == 'all' and partido_sigla is not None and partido_sigla <> 'all':
        ret = politicaServices.candidaturaByPartido(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = CandidaturaTotal.query.limit(limit).offset(offset).all()
    elif candidatura_id is not None and candidatura_id<>'all':
        ret = CandidaturaTotal.query.filter_by(candidatura=candidatura_id).limit(limit).offset(offset).all()
    else:
        ret = CandidaturaTotal.query.limit(limit).offset(offset).all()
       
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"candidaturas":items})
    else:
        return ''
    
@mod.route('/candidaturatime/<time_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/candidaturatime/<time_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_ccandidaturatime(time_id=None):
    ret = None
    if time_id is not None:
        ret = Candidatura.query.join(TimeCandidato).filter_by(time=time_id).all()
             
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"candidaturas":items})
    else:
        return ''
    
@mod.route('/pontuacaorodada/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacaorodada/<rodada_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacaorodada/<rodada_id>/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacaorodada/<rodada_id>/<candidatura_id>/<partido_sigla>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_pontuacaorodada(rodada_id=None,candidatura_id=None,partido_sigla=None):
    if candidatura_id is None:
        ret = Pontuacao.query.join(Rodada).filter_by(id=rodada_id).order_by(Pontuacao.rodada,Pontuacao.candidatura).all()
    elif candidatura_id == 'all' and partido_sigla is not None:
        ret = politicaServices.pontuacaoByPartido(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = Pontuacao.query.join(Rodada).filter_by(id=rodada_id).order_by(Pontuacao.rodada,Pontuacao.candidatura).all() 
    else:
        ret = Pontuacao.query.filter_by(candidatura=candidatura_id).\
        join(Rodada).filter_by(id=rodada_id).order_by(Pontuacao.rodada,Pontuacao.candidatura).all()
    
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"pontuacoes":items})
    else:
        return ''
       
@mod.route('/pontuacao/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacao/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacao/<candidatura_id>/<partido_sigla>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_pontuacao(candidatura_id=None,partido_sigla=None):
    if candidatura_id is None:
        ret = Pontuacao.query.filter_by(ativo=1).order_by(Pontuacao.rodada,Pontuacao.candidatura).all()
    elif candidatura_id == 'all' and partido_sigla is not None:
        ret = politicaServices.pontuacaoByPartido(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = Pontuacao.query.filter_by(ativo=1).order_by(Pontuacao.rodada,Pontuacao.candidatura).all() 
    else:
        ret = Pontuacao.query.filter_by(candidatura=candidatura_id,ativo=1).order_by(Pontuacao.rodada,Pontuacao.candidatura).all()
    
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"pontuacoes":items})
    else:
        return ''
    
@mod.route('/despesa/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/despesa/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/despesa/<candidatura_id>/<partido_sigla>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_despesa(candidatura_id=None,partido_sigla=None):
    if candidatura_id is None:
        ret = DespesaCandidato.query.join(Rodada).filter_by(ativo=1).all()
    elif candidatura_id == 'all' and partido_sigla is not None:
        ret = politicaServices.despesacandidato(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = DespesaCandidato.query.join(Rodada).filter_by(ativo=1).all() 
    else:
        ret = DespesaCandidato.query.filter_by(candidatura=candidatura_id,ativo=1)\
        .join(Rodada).filter_by(ativo=1).all()
             
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"despesas":items})
    else:
        return ''
    
@mod.route('/despesatipo/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_despesatipo():
    ret = DespesaTipo.query.all()
      
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"despesatipo":items})
    else:
        return ''

@mod.route('/pontuacaosum/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacaosum/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/pontuacaosum/<candidatura_id>/<partido_sigla>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_pontuacaosum(candidatura_id=None,partido_sigla=None):
    if candidatura_id is None:
        ret = politicaServices.pontuacaoSumRodadaByPartido(partido_sigla,candidatura_id) 
    elif candidatura_id == 'all' and partido_sigla is not None:
        ret = politicaServices.pontuacaoByPartido(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = Pontuacao.query.filter_by(ativo=1).all() 
    else:
        ret = Pontuacao.query.filter_by(candidatura=candidatura_id,ativo=1).all()
             
    if ret is not None:
        data = {}
        data[0]= 'rodada'
        data[1]= 'candidatura'
        data[2]= 'pontos'
        data[3]= 'presenca'
        data[4]= 'tendencia_presenca'
        data[5]= 'total_presenca'
        data[6]= 'proposicao'
        data[7]= 'tendencia_proposicao'
        data[8]= 'total_proposicao'
        data[9]= 'processo'
        data[10]= 'tendencia_processo'
        data[11]= 'total_processo'
        data[12]= 'votacao'
        data[13]= 'tendencia_votacao'
        data[14]= 'total_votacao'
        data[15]= 'despesa'
        data[16]= 'tendencia_despesa'
        data[17]= 'total_despesa'
        
        items = [serialize(keys=data,values=q) for q in ret]
        
    
        
        return jsonify({"pontuacoes":items})
    else:
        return ''





from datetime import datetime, date, timedelta
from decimal import Decimal

def serialize(values,keys):
    "Returns model's PUBLIC data for jsonify"
    data = {}
    i=0
    for k in  values:
        if isinstance(k, Decimal):
            value=float(k)        
        elif isinstance(k,unicode) or \
                                isinstance(k,float) or \
                                isinstance(k,int) or \
                                isinstance(k,str) or \
                                isinstance(k,long):
            value = _serialize(k)
        else: 
            value = _serialize(k)
        #value=k
        if value:
            data[keys[i]] = value
            
        
        i=i+1
    return data

def _serialize(value):
    if type(value) in (datetime, date):
        ret = value.isoformat()
    elif hasattr(value, '__iter__'):
        ret = []
        for v in value:
            ret.append(_serialize(v))    
    else:
        ret = value

    return ret

@mod.route('/partido/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/partido/<partido_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_partido(partido_id=None):
    ret = Partido.query.all()
    items = [q.serialize() for q in ret]
    return jsonify({"partidos":items})


@mod.route('/partidototal/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/partidototal/<ano>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_partidototal(ano=None):
    if ano is None:
        ret = PartidoTotal.query.outerjoin(Partido).all()
    else:
        ret = PartidoTotal.query.outerjoin(Partido).all()
    items = [q.serialize() for q in ret]
    return jsonify({"partidos":items})

@mod.route('/orgao/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/orgao/<partido_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_orgao(partido_id=None):
    ret = Orgao.query.all()
    items = [q.serialize() for q in ret]
    return jsonify({"orgaos":items})

@mod.route('/orgaocandidato/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/orgaocandidato/<orgao_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_orgaocandidato(orgao_id=None):
    ret = OrgaoCandidato.query.all()
    items = [q.serialize() for q in ret]
    return jsonify({"orgaocandidato":items})


@mod.route('/time/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/time/<time_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/time/<time_id>/<liga_id>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_time(time_id=None,liga_id=None):
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', 150)  
    
    if time_id is None and liga_id is None:
        ret = Time.query.order_by(Time.posicao).limit(limit).offset(offset).all()
    elif time_id=='all' and liga_id is not None:
        ret = Time.query.join(LigaJogador).filter_by(liga_ligajogador=liga_id).order_by(Time.posicao).limit(limit).offset(offset).all()
    else:
        ret = Time.query.filter_by(id=time_id).order_by(Time.posicao).limit(limit).offset(offset).all()
    items = [q.serialize() for q in ret]
    return jsonify({"times":items})



@mod.route('/top3time/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
def attrs_top3time():
    ret = politicaServices.top3Time()
    items = [q.serialize() for q in ret]
    return jsonify({"times":items})

@mod.route('/timecandidato/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/timecandidato/<time_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/timecandidato/<time_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/timecandidato/<time_id>/<candidatura_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/timecandidato/<time_id>/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_timecandidato(time_id=None,candidatura_id=None):
    if time_id is None:
        if candidatura_id is None:
            ret = TimeCandidato.query.all()
        else:
            ret = TimeCandidato.query.filter_by(candidatura=candidatura_id).all() 
    else:
        if candidatura_id is None:
            ret = TimeCandidato.query.filter_by(time=time_id).all()
        else:
            ret = TimeCandidato.query.filter_by(candidatura=candidatura_id,time=time_id).all()
    items = [q.serialize() for q in ret]
    return jsonify({"timecandidato":items})

@mod.route('/rodadapontos/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>/<rodada_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>/<rodada_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>/<rodada_id>/<liga_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodadapontos/<time_id>/<rodada_id>/<liga_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_rodadapontos(time_id=None,rodada_id=None,liga_id=None):
    if time_id is None:
        if rodada_id is None or rodada_id=="all":
            ret = RodadaPontos.query.filter_by(ativo=1).all()
        else:
            ret = RodadaPontos.query.filter_by(rodada=rodada_id,ativo=1).all() 
    else:
        if rodada_id is None or rodada_id=="all":
            ret = RodadaPontos.query.filter_by(time=time_id,ativo=1).all()
        else:
            ret = RodadaPontos.query.filter_by(ativo=1,rodada=rodada_id,time=time_id).all()
    items = [q.serialize() for q in ret]
    return jsonify({"rodadapontos":items})

@mod.route('/ligapontos/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/ligapontos/<liga_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/ligapontos/<liga_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/ligapontos/<liga_id>/<rodada_id>', methods=['GET','POST', 'OPTIONS'])
@mod.route('/ligapontos/<liga_id>/<rodada_id>/', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_ligapontos(liga_id=None,rodada_id=None):
    if liga_id is None:
        if rodada_id is None or rodada_id=="all":
            ret = LigaPontos.query.all()
        else:
            ret = LigaPontos.query.filter_by(rodada_ligapontos=rodada_id).all() 
    else:
        if rodada_id is None or rodada_id=="all":
            ret = LigaPontos.query.filter_by(liga_ligapontos=liga_id).all()
        else:
            ret = LigaPontos.query.filter_by(rodada_ligapontos=rodada_id,liga_ligapontos=liga_id).all()
    items = [q.serialize() for q in ret]
    return jsonify({"ligapontos":items})

@mod.route('/rodada/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/rodada/<rodada_id>/', methods=['GET','POST', 'OPTIONS'])
@crossdomain(origin='*')
@cross_origin(headers=['Content-Type'])
def attrs_rodada(rodada_id=None):
    if rodada_id is None:
        ret = Rodada.query.filter_by(ativo=1).all()
    else:
        ret = Rodada.query.filter_by(id=rodada_id).all()
    items = [q.serialize() for q in ret]
    return jsonify({"rodadas":items})

@mod.route('/votacaocandidato/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/votacaocandidato/<candidatura_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/votacaocandidato/<candidatura_id>/<partido_sigla>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_votacaocandidato(candidatura_id=None,partido_sigla=None):
    if candidatura_id is None:
        ret = VotacaoCandidato.query.all()
    elif candidatura_id == 'all' and partido_sigla is not None:
        ret = politicaServices.pontuacaoByPartido(partido_sigla) 
    elif candidatura_id == 'all' and partido_sigla is None:
        ret = VotacaoCandidato.query.all() 
    else:
        ret = VotacaoCandidato.query.filter_by(candidatura=candidatura_id).all()
             
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"votacaocandidato":items})
    else:
        return ''


@mod.route('/votacaoproposicao/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/votacaoproposicao/<proposicao_id>/', methods=['GET','POST', 'OPTIONS'])
@mod.route('/votacaoproposicao/<proposicao_id>/<candidatura_id>', methods=['GET','POST', 'OPTIONS'])
@cross_origin(headers=['Content-Type'])
@crossdomain(origin='*')
def attrs_votacaoproposicao(candidatura_id=None,proposicao_id=None):
    if proposicao_id is None:
        ret = VotacaoCandidato.query.join(Candidatura).all()
    elif proposicao_id == 'all' and candidatura_id is not None:
        ret = politicaServices.pontuacaoByPartido(candidatura_id) 
    elif proposicao_id == 'all' and candidatura_id is None:
        ret = VotacaoCandidato.query.join(Candidatura).all() 
    else:
        ret = VotacaoCandidato.query.filter_by(proposicao=proposicao_id).all()
             
    if ret is not None:
        items = [q.serialize() for q in ret]
        return jsonify({"votacaocandidato":items})
    else:
        return ''
    
#        SERVICOS: criarTime
@mod.route('/criar-partido/', methods=['GET', 'POST', 'OPTIONS'])
@crossdomain(origin='*', headers='Content-Type')
@cross_origin(headers=['Content-Type'])
def criarPartido():
    
    if request.json is None:
        print "SEM JSON"
        return "Sem JSON"
    
    if 'user' in request.json:
        user = request.json['user']
    if 'nome' in request.json:
        nome = request.json['nome']
    if 'desc' in request.json:
        desc = request.json['desc']
        
    user = User.query.filter_by(id=user).first_or_404()
    
    if user is not None:
        print "buscando "+str(user.id)+ " - "  + nome + " - " +desc
        timeRetorno = politicaServices.meuTime(user.id) 
        print "depois buscar"
        if timeRetorno is not None:
            print "TIME encontrado"
            return jsonify({"time":timeRetorno.serialize()})
    else:
        return jsonify({"user":"nao encontrado"})
   
    
    time = Time(nome=nome, desc=desc,  user_id=user.id)
    db.session.add(time)
    db.session.commit()
    return jsonify({"time":time.serialize()})

