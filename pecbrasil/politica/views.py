# -*- coding: utf-8 -*- 
from datetime import datetime
from sqlalchemy import func
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
import csv, sys, MySQLdb, os
from os import environ

from pecbrasil import db
from pecbrasil.utils import clean_varrequest
from pecbrasil.politica.forms import PoliticoForm,TimeForm
from pecbrasil.politica.models import Politico, Partido, TimeCandidato,Time, Rodada, RodadaPontos,Candidatura,Pontuacao
from pecbrasil.politica.services import PoliticaServices
from pecbrasil.comunicado.forms import ConvidarForm


mod = Blueprint('politica', __name__, url_prefix='/politica')
    
politicaServices = PoliticaServices()     

#  Ver a selecao de um time
@mod.route('/selecao/')
@mod.route('/selecao/<nome>')
@mod.route('/selecao/<nome>/<slug>')
def selecao(nome=None):
    # Quando nome-selecao for vazio mostrar a selecao do usuario logado
    rodada_atual = db.session.merge(session['rodada_atual'])
    if nome is not None:
        times = politicaServices.verTime(None,nome)            
        return render_template("politica/selecao.html",                rodada_atual=rodada_atual,              
                               time=times)
    else:
        times = politicaServices.verTime(g.user)
        return render_template("politica/selecaoList.html",         rodada_atual=rodada_atual,                       times = times)

    
#    Pagina-politico_detalhes
#        URL: /politica/politico/nome-fulano
#        ** Quando o nome-fulano for vazio, renderizar a lista dos top politico
#        HTML: html/politica/politico.html
#        HTML: html/politica/politicoList.html
@mod.route('/politico/', methods=['GET', 'POST'])
@mod.route('/politico/<nome>', methods=['GET', 'POST'])
@mod.route('/politico/<nome>/', methods=['GET', 'POST'])
@mod.route('/politico/<nome>/<order>', methods=['GET', 'POST'])
@mod.route('/politico/<nome>/<order>/', methods=['GET', 'POST'])
def politico(nome=None,order=None):
    
    rodada_atual = db.session.merge(session['rodada_atual'])
    orderdirec = request.args.get('orderdirec')
    estado = request.args.get('estado')
    form=PoliticoForm()
    
    if form.validate_on_submit(): 
        nome=form.nome.data
    
    politicos=politicaServices.verCandidatura(nome,order,orderdirec,estado)
    
    if politicos <> None and isinstance(politicos, list) and len(politicos)>1:
        url="politica/politicoList.html" 
    else:
        url="politica/politico.html"
        if  isinstance(politicos, list) and len(politicos)==1: politicos = politicos[0]
    
    return render_template(url,orderby=order, form=form,rodada_atual=rodada_atual,estado=estado,orderdirec=orderdirec,
                                politicos = politicos)
       
@mod.route('/resumopolitico/')
@mod.route('/resumopolitico/<nome>')
def resumopolitico(nome=None):
    politicos=politicaServices.verCandidatura(nome) 
    if politicos is not None:
        return render_template("politica/resumopolitico.html",politicos=politicos)
    else:
        return None        
        
#    card--politico
#        URL: /politica/boxpolitico
#        HTML: html/politica/boxPolitico.html
#        SERVICOS: Função que recebe de entrada o registro de candidatura e monta o box de politico
@mod.route('/boxpolitico/')
@mod.route('/boxpolitico/<nome>')
def boxpolitico(nome=None):
    politicos=politicaServices.verCandidatura(nome) 
    rodada_atual = db.session.merge(session['rodada_atual'])
    if politicos is not None:
        return render_template("politica/boxpoliticoFrame.html",candidato=politicos[0],rodada_atual=rodada_atual)
    else:
        return None
        
#    Pagina-ranking    
#        URL: /politica/classificacao/nome-liga
#        ** Quando o nome-liga for vazio, renderizar a lista da classificação geral
#        ** Quando preenchido o nome, exibir a liga, este recurso ainda não tem, mas ja deixar a view mapeada
#        HTML: html/politica/classificacao.html
#        SERVICOS: top3Time,topTimes, topPartidos,verTime
@mod.route('/classificacao/')
@mod.route('/classificacao/<nome>')
def classificacao(nome=None):
    top3Time= politicaServices.top3Time()
    
    num_lines=0
    primeiro=None
    segundo=None
    terceiro=None
    for line in top3Time:       
        num_lines += 1
        if num_lines == 1:
            primeiro = line
        elif num_lines == 2:
            segundo = line
        else:
            terceiro = line
        
    rodadaAtual= politicaServices.rodadaAtual()
    topTimes= politicaServices.topTimes()
    topPartidos=  politicaServices.partidosPopulares()
    verTime= politicaServices.verTime(g.user)
    if nome is None:
        return render_template("politica/classificacao.html",
                   top3Time=top3Time,topTimes=topTimes,primeiroTime=primeiro,segundoTime=segundo,
                   terceiroTime=terceiro,rodadaAtual=rodadaAtual,
                    topPartidos=topPartidos,verTime=verTime)

#        SERVICOS: criarTime
@mod.route('/criar-partido/', methods=['GET', 'POST'])
def criarPartido(name=None):
    
    time_form = TimeForm()
    if g.user is not None and g.user.is_authenticated():
        timeRetorno = politicaServices.meuTime(g.user.id) 
        if timeRetorno is not None:
            return redirect(url_for('politica.verPartido'))
    else:
        return redirect(url_for('account.login'))
        
    if time_form.validate_on_submit():       
    
        #if g.user is None or not g.user.is_authenticated():
        #    flash('You need to be signed in for this.')
        #    return redirect(url_for('general.access'))
        
        time = Time(nome=time_form.nome.data, desc=time_form.desc.data, 
                      color=time_form.color.data,  user_id=g.user.id)
        db.session.add(time)
        db.session.commit()
        session['user_time']=time.id
        return redirect(url_for('politica.selecionarPoliticos'))
    else:       
        return render_template("politica/criar-partido.html",time_form=time_form)

    
#    Pagina-Tutorial---Tela3---PEC-Brasil
#        URL: /politica/selecionar-politicos
#        HTML: html/politica/selecionarPoliticos.html
#        SERVICOS: associarPoliticoTime
@mod.route('/selecionar-politicos/', methods=['GET', 'POST'])
@mod.route('/selecionar-politicos/<idpolitico>', methods=['GET', 'POST'])
@mod.route('/selecionar-politicos/<idpolitico>/<posicao>', methods=['GET', 'POST'])
@mod.route('/selecionar-politicos/<idpolitico>/<posicao>/', methods=['GET', 'POST'])
@mod.route('/selecionar-politicos/<idpolitico>/<posicao>/<gravar>', methods=['GET', 'POST'])
def selecionarPoliticos(idpolitico=None,posicao=None,gravar=None):
    form=PoliticoForm()
    orderdirec = request.args.get('orderdirec')
    order = request.args.get('order')
    nome=None
    if form.validate_on_submit(): 
        nome=form.nome.data
        
    if nome is None:
        nome="all"
        
    if 'user_time' in session:
        time = session['user_time']
        rodada_atual = db.session.merge(session['rodada_atual'])
       
        if idpolitico is None or idpolitico=='0':
            politicos=politicaServices.verCandidatura(nome,order,orderdirec)
            print politicos
            print "eiola"
            #politicos = politicaServices.topPoliticos()
            politicosSelecionados=politicaServices.verTime(id=time)
            return render_template("politica/selecionar-politicos.html",form=form,rodada_atual=rodada_atual,orderby=order,orderdirec=orderdirec,
                        politicos = politicos,posicao=1,time=time,politicosSelecionados=politicosSelecionados)
        elif int(posicao) <=4:
            if gravar is None or gravar=="true" or gravar=="None":
                TimeCandidato.query.filter_by(time=time, posicao=posicao).delete()
                db.session.commit()
                timeCand = TimeCandidato(time=time, posicao=posicao,    candidatura=idpolitico)
                db.session.add(timeCand)
                db.session.commit()
                posicao=int(posicao)+1
  
            if  gravar=="true" or int(posicao) == 5:
                return redirect(url_for('politica.verPartido',time=time))
            if  gravar=="false":
                gravar="true"
            politicos=politicaServices.verCandidatura(nome,order,orderdirec)
            #politicos = politicaServices.topPoliticos()

            politicosSelecionados=politicaServices.verTime(id=time)

            return render_template("politica/selecionar-politicos.html",form=form,gravar=gravar,rodada_atual=rodada_atual,orderby=order,orderdirec=orderdirec,
                        politicos = politicos,posicao=int(posicao),time=time,politicosSelecionados=politicosSelecionados)
        else:
            TimeCandidato.query.filter_by(time=time, posicao=posicao).delete()
            return redirect(url_for('politica.verPartido',time=time))        
    else:
        
        #nao logado
        return redirect(url_for('general.home'))
    
#        SERVICOS: verTime
@mod.route('/meu-partido/', methods=['GET', 'POST'])
@mod.route('/meu-partido/<time>', methods=['GET', 'POST'])
def verPartido(time=None):
    form=ConvidarForm()
    
    if g.user is None or not g.user.is_authenticated():
        return   redirect(url_for('politica.criarPartido'))
    
    timeRetorno = politicaServices.meuTime(g.user.id) 
    if timeRetorno is None:
        return   redirect(url_for('politica.criarPartido'))
    
    time_form = TimeForm()
    if time_form.validate_on_submit(): 
        timeRetorno.nome=time_form.nome.data
        timeRetorno.desc=time_form.desc.data
        db.session.add(timeRetorno)
        db.session.commit()
        
    session['user_time']=timeRetorno.id
    rodaA = db.session.merge(session['rodada_atual'])
    
    time_form.nome.data=timeRetorno.nome
    time_form.desc.data=timeRetorno.desc
    
    
        
    return render_template("politica/meu-partido.html",  rodada_atual=rodaA ,  time_form=time_form, form=form,            time = timeRetorno,user=g.user, time_id=time)


 
 
### ### ### ### ### ### ### ### ###  
### TESTES ###
### ### ### ### ### ### ### ### ### 

@mod.route('/partido/')
@mod.route('/partidos/')
@mod.route('/partido/<name>')
def partido(name=None):    
    if name is not None:
        partidos = Partido.query.filter_by( id=name).first()
        return render_template("politica/partido.html",
                        partidos = partidos)
    else:
        partidos = Partido.query.all()
        return render_template("politica/partidoList.html",
                        partidoList = partidos)
        
@mod.route('/resumopartido/')
@mod.route('/resumopartido/<nome>')
def resumopartido(name=None):
    if name is not None:
        partidos = Partido.query.filter_by( id=name).first()
        return render_template("politica/resumopartido.html",
                        partidos = partidos)
    else:
        partidos = Partido.query.all()
        return render_template("politica/resumopartidoList.html",
                        partidoList = partidos)
      

@mod.route('/time/')
@mod.route('/time/<name>')
def time(name=None):
    if name is not None:
        times = Time.query.first()
        return render_template("politica/time.html",
                        times = times)
    else:
        times = Time.query.all()
        return render_template("politica/timeList.html",
                        times = times)

@mod.route('/candidatura/')
@mod.route('/candidatura/<name>')
def candidatura(name=None):
    if name is not None:
        candidaturas = Candidatura.query.first()
        return render_template("politica/candidatura.html",
                        candidaturas = candidaturas)
    else:
        candidaturas = Candidatura.query.all()
        return render_template("politica/candidaturaList.html",
                        candidaturas = candidaturas)
        
@mod.route('/pontuacao/')
@mod.route('/pontuacao/<name>')
def pontuacao(name=None):
    if name is not None:
        pontuacoes = Pontuacao.query.first()
        return render_template("politica/pontuacao.html",
                        pontuacoes = pontuacoes)
    else:
        pontuacoes = Pontuacao.query.all()
        return render_template("politica/pontuacaoList.html",
                        pontuacoes = pontuacoes)

@mod.route('/excluirtime')
@mod.route('/excluirtime/')
def excluirtime():
    time = session['user_time']
    if time is None:
        time= politicaServices.verTime(g.user)
        time = Time.query.filter_by(id=time.id).delete()
    else:
        Time.query.filter_by(id=time).delete()
    db.session.commit()
    return redirect(url_for('politica.criarPartido'))

