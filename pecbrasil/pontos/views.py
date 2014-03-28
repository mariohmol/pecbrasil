# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
import csv, sys, MySQLdb, os
from os import environ

from pecbrasil import db
from pecbrasil.politica.forms import PoliticoForm,TimeForm
from pecbrasil.politica.models import Politico, Partido, TimeCandidato,Time, Rodada, RodadaPontos,Candidatura,Pontuacao
from pecbrasil.politica.services import PoliticaServices

mod = Blueprint('pontos', __name__, url_prefix='/pontos')
    
politicaServices = PoliticaServices()     

@mod.route('/politico/')
@mod.route('/politico/<nome>')
@mod.route('/politico/<nome>/<frame>')
def politico(nome=None,frame=None):
    if nome is not None:
        politicos = politicaServices.pontoByPolitico(nome)
        return render_template("pontos/politico.html",        frame=frame,             politicos = politicos )
    else:
        politicos = politicaServices.pontoByPolitico(nome)
        return render_template("pontos/politicoList.html",     frame=frame,                           politicos = politicos)

    
@mod.route('/time/')
@mod.route('/time/<nome>')
@mod.route('/time/<nome>/<frame>')
def time(nome=None,frame=None):
    times=politicaServices.pontoTimes(nome)
    if nome is not None:                
        return render_template("pontos/time.html", frame=frame,
                                times = times)
    else:     
        return render_template("pontos/timeList.html",frame=frame,
                               times = times )
       

@mod.route('/rodada/')
@mod.route('/rodada/<nome>')
@mod.route('/rodada/<nome>/<frame>')
def rodada(nome=None,frame=None):
    rodadas=politicaServices.pontoRodada(nome)
    return render_template("pontos/rodadaList.html",frame=frame,
                               rodadas = rodadas)
       
@mod.route('/pontuacaorodada/')
@mod.route('/pontuacaorodada/<nome>')
@mod.route('/pontuacaorodada/<nome>/<frame>')
def pontuacaorodada(nome=None,frame=None):
    rodadas=politicaServices.pontoPoliticoRodada(nome)
    return render_template("pontos/pontuacaorodada.html",frame=frame,
                               rodadas = rodadas)
