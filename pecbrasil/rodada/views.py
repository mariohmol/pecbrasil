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

mod = Blueprint('rodada', __name__, url_prefix='/rodada')
    
politicaServices = PoliticaServices()     


@mod.route('/')
@mod.route('/ver/<name>')
def rodada(name=None):
    rodadas = politicaServices.rodadas(name)
    
    if name is not None:
        anterior=politicaServices.anteriorRodada(inicio=rodadas.inicio)
        proximo=politicaServices.proximaRodada(inicio=rodadas.inicio)
        
        return render_template("rodada/rodada.html",
                    rodadas = rodadas,anterior=anterior,proximo=proximo)
    else:
        return render_template("rodada/rodadaList.html",
                    rodadas = rodadas)

@mod.route('/rodadapontos/')
@mod.route('/rodadapontos/<name>')
def rodadapontos(name=None):
    
    if name is not None:
        rodadapontos = RodadaPontos.query.first()
        return render_template("rodada/rodadapontos.html",
                            rodadapontos = rodadapontos)
    else:
        rodadapontos = RodadaPontos.query.all()
        return render_template("rodada/rodadapontosList.html",
                            rodadapontos = rodadapontos)

