#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
import csv, sys, MySQLdb, os
from os import environ

from pecbrasil import db
from pecbrasil.politica.forms import PoliticoForm,TimeForm
from pecbrasil.politica.models import Politico, Partido, TimeCandidato,Time, Rodada, RodadaPontos,Candidatura,Pontuacao
from pecbrasil.proposicao.models import Proposicao
from pecbrasil.politica.services import PoliticaServices

mod = Blueprint('politico', __name__, url_prefix='/politico')
    
politicaServices = PoliticaServices()     


import unicodedata as ud


@mod.route('/votacao/')
@mod.route('/votacao/<candidatura_id>')
@mod.route('/votacao/<candidatura_id>/')
@mod.route('/votacao/<candidatura_id>/<partido_sigla>')
@mod.route('/votacao/<candidatura_id>/<partido_sigla>/<frame>')
def votacaocandidato(candidatura_id=None,partido_sigla=None,frame=None):
    # VotacaoCandidato
    #test=ud.name(u'\xe9')
    test=""
    votacoes = politicaServices.votacaoCandidatura(candidatura_id,partido_sigla)
    #for vota in votacoes:
    #    test=test+vota.proposicoes.desc
    #test=unicode(test)
    #test=test.encode('utf-8')
    
    
    #test = test.decode('cp1250')
    #test = test.encode('utf8')

    if candidatura_id is not None:        
        return render_template("politico/votacaocandidato.html",  
                               test=test, iframe=frame,
                                votacoes = votacoes )
    else:
        return render_template("politico/votacaocandidatoList.html",   iframe=frame,      votacoes = votacoes)
    
@mod.route('/repasse/')
@mod.route('/repasse/<candidatura_id>')
@mod.route('/repasse/<candidatura_id>/')
@mod.route('/repasse/<candidatura_id>/<partido_sigla>')
def repasse(candidatura_id=None,partido_sigla=None):
    # Repasse
    repasses = politicaServices.repasse(candidatura_id,partido_sigla)
    if candidatura_id is not None:
        return render_template("politico/repasse.html",     repasses = repasses )
    else:
        return render_template("politico/repasseList.html",     repasses = repasses)
    
    
       
@mod.route('/despesa/')
@mod.route('/despesa/<candidatura_id>')
@mod.route('/despesa/<candidatura_id>/')
@mod.route('/despesa/<candidatura_id>/<partido_sigla>')
def despesacandidato(candidatura_id=None,partido_sigla=None):
    # DespesaCandidato
    despesas = politicaServices.despesacandidato(candidatura_id=candidatura_id,partido_sigla=partido_sigla)
    if candidatura_id is not None:
        return render_template("politico/despesacandidato.html",                         
                                    despesas = despesas ,partido_sigla=partido_sigla,candidatura_id=candidatura_id)
    else:
        return render_template("politico/despesacandidatoList.html",   despesas = despesas,partido_sigla=partido_sigla ,candidatura_id=candidatura_id)
    
@mod.route('/processo/')
@mod.route('/processo/<candidatura_id>')
@mod.route('/processo/<candidatura_id>/')
@mod.route('/processo/<candidatura_id>/<partido_sigla>')
def processocandidato(candidatura_id=None,partido_sigla=None):
    # ProcessoCandidato
    processos = politicaServices.processocandidato(candidatura_id,partido_sigla)
    
    if candidatura_id is not None:
        
        return render_template("politico/processocandidato.html",                         
                                    processos = processos )
    else:
        return render_template("politico/processocandidatoList.html",   processos = processos)


  




