# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlalchemy import func,update
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
import csv, sys, MySQLdb, os
from os import environ
import datetime

from pecbrasil import db
from pecbrasil.liga.forms import LigaForm
from pecbrasil.proposicao.forms import AvaliarForm
from pecbrasil.proposicao.models import TimeVotacao,Proposicao,VotacaoCandidato
from pecbrasil.liga.models import Liga,LigaPontos,LigaJogador
from pecbrasil.politica.services import PoliticaServices

mod = Blueprint('proposicao', __name__, url_prefix='/proposicao')
    
politicaServices = PoliticaServices()     

@mod.route('/votar/<proposicao>/<voto>/<necessidade>', methods=['GET', 'POST'])
def votar(proposicao=None,voto=None):
    if proposicao is not None:
        proposicaoObj =  Proposicao.query.filter_by(id=proposicao).first() 
    
    meuTime = politicaServices.meuTime(userId=g.user.id)
    
    if meuTime is not None and proposicaoObj is not None:        
        timeVotacao = TimeVotacao(    desc=liga_form.nome.data, 
                        data=datetime.datetime.now(), 
                        proposicao=proposicaoObj.id, 
                        time = meuTime.id,
                        data_liga=datetime.datetime.now(), 
                        voto=voto)
        db.session.add(timeVotacao)
        db.session.commit()
    return render_template("liga/liga.html",liga=liga)

@mod.route('/avaliar/<proposicaoid>', methods=['GET', 'POST'])
def avaliar(proposicaoid=None):
    if g.user is None or not g.user.is_authenticated():
        flash('You need to be signed in for this.')
        return redirect(url_for('account.login'))
    proposicoes = Proposicao.query.filter_by(id=proposicaoid).first()    
    meuForm = AvaliarForm(request.form)
    meuTime = politicaServices.meuTime(userId=g.user.id)  
    if request.method == 'POST' and meuForm.validate_on_submit():
        timeVot = TimeVotacao.query.filter_by(time = meuTime.id, proposicao = proposicaoid).first()
        if timeVot is None:
            timeVot = TimeVotacao(desc=meuForm.desc.data,  voto=meuForm.voto.data, data=datetime.datetime.now(), \
                              time = meuTime.id, proposicao = proposicaoid,necessidade=meuForm.necessidade.data)            
            db.session.add(timeVot)
        else:
            timeVot.data=datetime.datetime.now()
            timeVot.necessidade=meuForm.necessidade.data
            timeVot.desc=meuForm.desc.data
            timeVot.voto=meuForm.voto.data
        
        db.session.commit()
        return verproposicao(proposicao_id=proposicaoid)    
    return render_template("proposicao/avaliar.html" , \
                           proposicaoid = proposicaoid,
                           meuForm=meuForm,proposicoes=proposicoes)

@mod.route('/listar/')
@mod.route('/listar/<candidatura_id>')
@mod.route('/listar/<candidatura_id>/')
@mod.route('/listar/<candidatura_id>/<partido_sigla>')
@mod.route('/listar/<candidatura_id>/<partido_sigla>/<frame>')
def proposicao(candidatura_id=None,partido_sigla=None,frame=None):
    # Proposicao
    proposicoes = politicaServices.proposicao(candidatura_id,partido_sigla)
        
    return render_template("proposicao/proposicaoList.html",                proposicoes = proposicoes, frame=frame)
 
    
@mod.route('/ver/')
@mod.route('/ver/<proposicao_id>')
@mod.route('/ver/<proposicao_id>/')
def verproposicao(proposicao_id=None):
    
    proposicoes = Proposicao.query.filter_by(id=proposicao_id).first()
        
    if proposicao_id is not None:
        return render_template("proposicao/proposicao.html",      proposicoes=proposicoes)                   
    

@mod.route('/listarvotacao/')
@mod.route('/listarvotacao/<proposicao_id>')
@mod.route('/listarvotacao/<proposicao_id>/')
@mod.route('/listarvotacao/<proposicao_id>/<candidatura_id>')
@mod.route('/listarvotacao/<proposicao_id>/<candidatura_id>/<frame>')
def listarvotacao(candidatura_id=None,proposicao_id=None,frame=None):
   
    votacoes = politicaServices.votacao(proposicao_id,candidatura_id)
        
    return render_template("proposicao/votacaoList.html",                votacoes = votacoes, frame=frame)
 
    
@mod.route('/votacao/')
@mod.route('/votacao/<proposicao_id>')
@mod.route('/votacao/<proposicao_id>/')
def votacao(proposicao_id=None):
    
    votacoes = VotacaoCandidato.query.filter_by(proposicao=proposicao_id).first()
        
    if proposicao_id is not None:
        return render_template("proposicao/votacao.html",      votacoes=votacoes) 
    
@mod.route('/acao/')
@mod.route('/acao/<proposicao_id>')
@mod.route('/acao/<proposicao_id>/<candidatura_id>')
@mod.route('/acao/<proposicao_id>/<candidatura_id>/<partido_id>')
def acao(proposicao_id=None,candidatura_id=None,partido_id=None):
    
    dataInicio = request.args.get('inicio')
    frame = request.args.get('frame')
    #if dataInicio is None:
    #    dataInicio= "01/10/2010"
    if proposicao_id:
        acoes = politicaServices.proposicaoacao(dataInicio,proposicao_id=proposicao_id,candidatura_id=candidatura_id,partido_sigla=partido_id)
    else:
        acoes      = politicaServices.ultimasProposicaoacao()
    if len(acoes)>1:
        return render_template("proposicao/acaoList.html",      acoes=acoes,frame=frame) 
    else:
        return render_template("proposicao/acao.html",      acoes=acoes,frame=frame) 
    
@mod.route('/novidades/')
@mod.route('/novidades/<proposicao_id>')
@mod.route('/novidades/<proposicao_id>/<candidatura_id>')
@mod.route('/novidades/<proposicao_id>/<candidatura_id>/<partido_id>')
def novidades(proposicao_id=None,candidatura_id=None,partido_id=None):
    
    dataInicio = request.args.get('inicio')
    frame = request.args.get('frame')
    #if dataInicio is None:
    #    dataInicio= "01/10/2010"
    if proposicao_id:
        acoes = politicaServices.proposicaoacao(dataInicio,proposicao_id=proposicao_id,candidatura_id=candidatura_id,partido_sigla=partido_id)
    else:
        acoes      = politicaServices.ultimasProposicaoacao()
        
    votacoes      = politicaServices.ultimasProposicaovotacao()
    return render_template("proposicao/ultimasacoes.html",      acoes=acoes , votacoes=votacoes,frame=frame) 

