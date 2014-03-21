# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
import csv, sys, MySQLdb, os
from os import environ
import datetime

from pecbrasil import db
from pecbrasil.liga.forms import LigaForm
from pecbrasil.liga.models import Liga,LigaPontos,LigaJogador
from pecbrasil.politica.services import PoliticaServices
from pecbrasil.comunicado.forms import ConvidarForm

mod = Blueprint('liga', __name__, url_prefix='/liga')
    
politicaServices = PoliticaServices()     

@mod.route('/criar/', methods=['GET', 'POST'])
def criar(nome=None):
    liga_form = LigaForm()
    if g.user is not None and g.user.is_authenticated():
        timeRetorno = politicaServices.meuTime(g.user.id) 
        if timeRetorno is None:
            return redirect(url_for('politica.criarPartido'))
    else:
        return redirect(url_for('account.login'))
    if liga_form.nome.data is not None:
        #liga_form.validate_on_submit():       
        #timestamp = datetime.utcnow()
        ligaExiste = politicaServices.liga(nome=liga_form.nome.data)
        if ligaExiste is not None:
            return render_template("liga/criar-liga.html",liga_form=liga_form,erromsg="Ja existe uma liga com este nome")
        liga = Liga(    nome_liga=liga_form.nome.data, 
                        desc_liga=liga_form.desc.data, 
                        publico_liga=liga_form.publico.data, 
                        data_liga=datetime.datetime.now(), 
                        criador_liga=timeRetorno.id)
        db.session.add(liga)
        
        db.session.commit()
        idliga= liga.id_liga
        ligaJog = LigaJogador(data_ligajogador=datetime.datetime.now(),
                    user_ligajogador=timeRetorno.id,
                    liga_ligajogador=liga.id_liga)
        db.session.add(ligaJog)
        db.session.commit()

        return ver(idliga)
        #redirect(url_for('liga.ver')+str(15))
    else:       
        return render_template("liga/criar-liga.html",liga_form=liga_form)

from flask.ext.mail import Message
from config import ADMINS
from pecbrasil import mail


@mod.route('/')
@mod.route('/ver')
@mod.route('/ver/')
@mod.route('/ver/<id>')
@mod.route('/ver/<id>/')
@mod.route('/ver/<id>/<nome>')
def ver(id=None,nome=None):
    #msg = Message('test subject', sender = ADMINS[0], recipients = ADMINS)
    #msg.body = 'text body'
    #msg.html = '<b>HTML</b> body'
    #with app.app_context():
    #    mail.send(msg)
     
    form=ConvidarForm()
    # Quando nome-selecao for vazio mostrar a selecao do usuario logado
    if id is not None:
        liga = Liga.query.filter_by(id_liga = id).all()
        if liga is None:
            liga = Liga.query.filter_by(nome_liga = nome).all()
        
        if liga is not None and len(liga)>0:
            time=getusertime()
            return render_template("liga/liga.html",  meutime=time, liga = liga[0] )
    else:
        ligas = Liga.query.all()   
        return render_template("liga/ligaList.html",   ligas = ligas,form=form)

@mod.route('/convidar/<liga>')
@mod.route('/convidar/<liga>/')
@mod.route('/convidar/<liga>/<nome>')
@mod.route('/convidar/<liga>/<nome>/')
def convidar(liga=None,nome=None):
    
    if g.user is None or not g.user.is_authenticated():
        return jsonify({"error": gettext("You need to be logged in to vote.")})
    
    msg = Message("Hello",
                  sender="pecbrcontato@gmail.com",
                  recipients=["pecbrasil@googlegroups.com","rafaelbuiu@gmail.com","mariohmol@gmail.com"])   
    msg.body = "Test de Convidar mandando email. usuario: {0} convida {1} para a liga".format(nome, liga)
    msg.html = msg.body #"+g.user.id+ "
    mail.send(msg)
    return None

@mod.route('/entrar/<liga>') 
@mod.route('/entrar/<liga>/')
@mod.route('/entrar/<liga>/<nome>')
def entrar(liga=None,nome=None):
    # Quando nome-selecao for vazio mostrar a selecao do usuario logado
    if liga is not None:
        ligaObj = Liga.query.filter_by(id_liga = liga).all()
        if ligaObj is None or not g.user.is_authenticated() :
            return redirect(url_for('account.login'))
        time = politicaServices.meuTime( g.user.id)
        ligaJog = LigaJogador.query.filter_by(liga_ligajogador = liga, 
                                              user_ligajogador = time.id).all()

        if ligaJog is None or len(ligaJog)==0:
            ligaJog = LigaJogador(data_ligajogador=datetime.datetime.now(),
                    user_ligajogador=time.id,
                    liga_ligajogador=ligaObj[0].id_liga)
            db.session.add(ligaJog)
            db.session.commit()
        return redirect(url_for('liga.ver')+liga)
    #render_template("liga/liga.html", liga = ligaObj[0]  )

@mod.route('/excluir/<liga>')
def excluir(liga):
    ligaObj = Liga.query.filter_by(id_liga = liga).first()
    if ligaObj is None:
        return None
    
    time = getusertime()
    if ligaObj.criador_liga == time:
        Liga.query.filter_by(id_liga = liga).delete()
        db.session.commit()
    else:
        redirect(url_for('liga.ver')+liga)
    return redirect(url_for('liga.criar'))

def getusertime():
    time=None
    if 'user_time' in session:
        time=session['user_time']
    print g.user
    if time is None and g.user.is_authenticated():
        time = politicaServices.meuTime(g.user.id)                
        session['user_time']=time
    return time

@mod.route('/excluirjogador/<liga>/<jogador>')
def excluirjogador(liga,jogador):
    ligaObj = Liga.query.filter_by(id_liga = liga).first()
    if ligaObj is None:
        return None
    
    time = getusertime()
    if ligaObj.criador_liga == time:
        LigaJogador.query.filter_by(user_ligajogador=jogador,    liga_ligajogador = liga).delete()
        db.session.commit()  
        
    return redirect(url_for('liga.ver')+liga)

@mod.route('/sairliga/<liga>')
def sairliga(liga=None):
    if liga is not None:
        ligaObj = Liga.query.filter_by(id_liga = liga).all()
        if ligaObj is None or not g.user.is_authenticated() :
            return redirect(url_for('account.login'))
        time = politicaServices.meuTime( g.user.id)
        ligaJog = LigaJogador.query.filter_by(liga_ligajogador = liga, 
                                              user_ligajogador = time.id).delete()
        db.session.commit()
    return redirect(url_for('liga.ver')+liga)
                

@mod.route('/mudarvisivel/<liga>')
def mudarvisivel(liga):
    ligaObj = Liga.query.filter_by(id_liga = liga).first()
    if ligaObj is None:
        return None
    
    time = getusertime()
    if ligaObj.criador_liga == time:
        if ligaObj.publico_liga == 1:
            ligaObj.publico_liga=0
        else:
            ligaObj.publico_liga=1
        db.session.add(ligaObj)
        db.session.commit()  
        
    return redirect(url_for('liga.ver')+liga)