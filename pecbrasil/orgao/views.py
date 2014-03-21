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
from pecbrasil.orgao.models import Orgao,OrgaoCandidato
from pecbrasil.liga.models import Liga,LigaPontos,LigaJogador
from pecbrasil.politica.services import PoliticaServices

mod = Blueprint('orgao', __name__, url_prefix='/orgao')
    
politicaServices = PoliticaServices()     

@mod.route('/')
@mod.route('/listar/')
@mod.route('/listar/<candidatura_id>')
@mod.route('/listar/<candidatura_id>/')
@mod.route('/listar/<candidatura_id>/<partido_sigla>')
@mod.route('/listar/<candidatura_id>/<partido_sigla>/<frame>')
def orgao(candidatura_id=None,partido_sigla=None,frame=None):
    # Proposicao
    orgao = politicaServices.orgao(candidatura_id,partido_sigla)
        
    return render_template("orgao/orgaoList.html",                orgao = orgao, frame=frame)
 
    
@mod.route('/ver/')
@mod.route('/ver/<orgao_id>')
@mod.route('/ver/<orgao_id>/')
def verorgao(orgao_id=None):
    
    orgao = Orgao.query.filter_by(id=orgao_id).first()
        
    if orgao_id is not None:
        return render_template("orgao/orgao.html",      orgao=orgao)                   

 
@mod.route('/membros/')
@mod.route('/membros/<orgao_id>')
@mod.route('/membros/<orgao_id>/')
@mod.route('/membros/<orgao_id>/<frame>')
@mod.route('/membros/<orgao_id>/<frame>/')
def membros(orgao_id=None,frame=None):
    
    orgao = OrgaoCandidato.query.filter_by(orgao=orgao_id).all()
        
    if orgao_id is not None:
        print "ENMTREEIII"
        return render_template("orgao/orgaocandidatoList.html",   frame=frame,   orgao=orgao)                   
       
    
@mod.route('/tramitacao/')
@mod.route('/tramitacao/<proposicao_id>')
@mod.route('/tramitacao/<proposicao_id>/')
def tramitacao(proposicao_id=None):
    
    votacoes = VotacaoCandidato.query.filter_by(proposicao=proposicao_id).first()
        
    if proposicao_id is not None:
        return render_template("proposicao/votacao.html",      votacoes=votacoes) 