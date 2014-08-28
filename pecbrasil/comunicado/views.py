# -*- coding: utf-8 -*-
from sqlalchemy import func, distinct
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
from datetime import datetime, timedelta

from pecbrasil import db
from pecbrasil.politica.models import Candidatura, Pontuacao,Time,Rodada,RodadaPontos
from pecbrasil.liga.models import Convite
from pecbrasil.liga.models import LigaJogador
from pecbrasil.politica.models import Time
from pecbrasil.account.models import User

from pecbrasil.utils import exist_or_404, gzip_data, cached_query
from pecbrasil.politica.services import PoliticaServices
from pecbrasil.comunicado.forms import ConvidarForm
from flask.ext.mail import Message
from config import ADMINS
from pecbrasil import mail
from pecbrasil.utils import send_mail
from sqlalchemy import not_

mod = Blueprint('comunicado', __name__, url_prefix='/comunicado')
politicaServices = PoliticaServices()   

@mod.route('/convideamigos/', methods=['GET', 'POST'])
@mod.route('/convideamigos/<time_id>', methods=['GET', 'POST'])
def convideamigos(time_id=None):  
    titulo="Convite para o Politica Esporte Clube"
    print titulo
    form=ConvidarForm()
    if form.validate_on_submit():
        time = politicaServices.meuTime(g.user.id) 
        emails = form.email.data.split(',')
        
        for email in emails:
            try:                
                print send_mail(titulo,[email],   
                                render_template("comunicado/convideamigos.html",
                                                form=form,time=time,obs=form.obs.data, nome=form.nome.data))
            except:
                print "Error EMail"
            convite = Convite(email=email,dataenvio=datetime.now(),usuario=g.user.id)
            db.session.add(convite)        
            db.session.commit()
        return render_template("comunicado/convideamigosform.html",titulo=titulo,enviado='S',form=form) 
    else:
        return render_template("comunicado/convideamigosform.html",form=form)        

@mod.route('/ultimarodada')
@mod.route('/ultimarodada/<rodada_id>')
@mod.route('/ultimarodada/<rodada_id>/<time_id>')
def ultimarodada(rodada_id=None,time_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='True'
    rodada=politicaServices.getRodada(rodada_id)
    if rodada is None:
        return
    rodada_id=rodada.id
    total=0
    
    dominio=""
    #dominio="http://localhost:8084" 
    politicos=politicaServices.topPoliticosRodada(tamanho=5)
    rodada_atual = db.session.merge(session['rodada_atual'])
    titulo="Veja sua pontuação da rodada"
    log=""
    if time_id is not None and time_id<>"all":
        time = politicaServices.verTime(id=time_id)
        if time is not None:
            log = log + enviaUltimaRodada(time,rodada_id,titulo,
                                          rodada,politicos,rodada_atual,enviar)
            rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
            return render_template("comunicado/ultimarodada.html",dominio=dominio,
                                   time=time,rodada=rodada,rodadaPontos=rodadaPontos,
                                   politicos=politicos,rodada_atual=rodada_atual)
    else:
        times = Time.query.all()
        total=0
        for time in times:
            total=total+1
            log = log + enviaUltimaRodada(time,rodada_id,titulo,rodada,politicos,rodada_atual,enviar)
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log)

def enviaUltimaRodada(time,rodada_id,titulo,rodada,politicos,rodada_atual,enviar):
    
    log=""
    if time is not None and time.user is not None:
        
        #log=log+"\n"+str(time.user.email)+ " - "+str(time.id)+" - "+str(time.nome)
        rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
        if enviar == 'True':
            try:
                send_mail(titulo,[time.user.email],  
                      render_template("comunicado/ultimarodada.html",time=time,
                                      rodada=rodada,rodadaPontos=rodadaPontos,
                                      politicos=politicos,rodada_atual=rodada_atual))
            except:
                    print "Error EMail"
    return log  

@mod.route('/timeincompleto/')
@mod.route('/timeincompleto/<time_id>')
def timeincompleto(time_id=None): 
    titulo="Complete seu time"
    log=""
    enviar = request.args.get('enviar')
    total=0
    if enviar is None:
        enviar='True'
    rows=politicaServices.timesFaltandoPolitico()
    for row in rows:
        timeid=row[0]
        time = politicaServices.verTime(id=timeid)
        if enviar == 'True':
                try:
                    send_mail(titulo,[time.user.email],  
                              render_template("comunicado/timeincompleto.html",time=time))
                except:
                    print "Error EMail"
            
        log=log+","+str(time.user.email)
        total=total+1
    if time_id is not None:
        return render_template("comunicado/timeincompleto.html",time=time)
    else:
        return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)  
            
@mod.route('/abrecampeonato/')
@mod.route('/abrecampeonato/<time_id>')
def abrecampeonato(time_id=None): 
    titulo="Abertura do Campeonato"
    total=0
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        
        if time is not None:
            send_mail(titulo,[time.user.email],   
                      render_template("comunicado/abrecampeonato.html",time=time))
            total=total+1
            log=log+","+time.user.email

    else:
        times = Time.query.all()
        for time in times:
            if time is not None and time.user.email is not None:
                total=total+1
                log=log+","+time.user.email
                print "Enviando "+time.user.email
                try: 
                    send_mail(titulo,[time.user.email],  render_template("comunicado/abrecampeonato.html",time=time))
                except:
                    print "Unexpected error:"
              
    
    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log, time=time)   


@mod.route('/criartime/')
@mod.route('/criartime/<time_id>')
def criartime(time_id=None): 
    titulo="Crie seu time"
    total=0
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        if time is not None: # time.user.email
            try:
                send_mail(titulo,[time.user.email],   render_template("comunicado/criartime.html",time=time))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email
    else:
        #rows = db.session.execute("select email, nickname, fullname from account_user where id not in (select user_id from time)").first()
        times = Time.query.all()
        lista_user_id =[]
        for time in times:
            lista_user_id.append(int(time.user_id))
        #print lista_user_id
        rows = User.query.filter(not_(User.id.in_(lista_user_id))).all()
        #print rows
        
        
        total=0
        for row in rows:
            try:
                send_mail(titulo,[row.email],  
                          render_template("comunicado/criartime.html", 
                                          email=row.email, nickname=row.nickname,fullname=row.fullname))
            except:
                print "Unexpected error:"
                print "Error EMail"  +","+str([row.email])
            total=total+1
            log=log+", id em User "+str(row.id)+": "+str(row.email)
               
    
    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)    


@mod.route('/retornar/')
@mod.route('/retornar/<time_id>')
def retornar(time_id=None): 
    titulo="Faz tempo que vc nao joga, vamos voltar?"
    total=0
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        if time is not None:
            try:
                send_mail(titulo,[time.user.email],   
                          render_template("comunicado/retornar.html",time=time))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email
    else:
        if User.last_seen is not None:
            data = datetime.utcnow() - timedelta(days=30)
            rows = User.query.filter(data >= User.last_seen).all()
        #db.session.execute("select email, nickname, fullname from account_user where last_seen < date_sub(now(), interval 1 month)")
        #rows = db.session.fetchall()
            total=0
            for row in rows:
                try:
                    send_mail(titulo,[row.email],  
                          render_template("comunicado/retornar.html",nickname=row.nickname,fullname=row.fullname, email=row.email)) 
                except:
                    print "Unexpected error:"
                    print "Error EMail"
                total=total+1
                log=log+"," + str(row.email) # +time.user.email

    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)   


@mod.route('/politicoultimarodada') # Já existe um comunicado para última rodada para time
@mod.route('/politicoultimarodada/<rodada_id>')
@mod.route('/politicoultimarodada/<rodada_id>/<candidato_id>')
def politicoultimarodada(rodada_id=None,candidato_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='True'
    rodada=politicaServices.getRodada(rodada_id)
    if rodada is None:
        return
    rodada_id=rodada.id
    total=0
      
    dominio=""
    #dominio="http://localhost:8084"
    politicos_pontos = politicaServices.topPoliticosRodada(tamanho=5)
    politicos_presenca = politicaServices.topPoliticosPresenca(rodada_id, tamanho=5)
    politicos_votacao = politicaServices.topPoliticosVotacoes(rodada_id, tamanho=5)
    politicos_proposicao = politicaServices.topPoliticosProposicao(rodada_id, tamanho=5)
    politicos_despesa = politicaServices.topPoliticosDespesa(rodada_id, tamanho=5)
    
    media_pontos = Candidatura.query.with_entities(func.avg(Candidatura.pontuacao_ultima).label("media"))
    media_presenca= Pontuacao.query.with_entities(func.avg(Pontuacao.presenca)).filter(Pontuacao.rodada==rodada_id)[0][0]
    media_votacao= Pontuacao.query.with_entities(func.avg(Pontuacao.votacao)).filter(Pontuacao.rodada==rodada_id)[0][0]
    media_proposicao= Pontuacao.query.with_entities(func.avg(Pontuacao.proposicao)).filter(Pontuacao.rodada==rodada_id)[0][0]
    media_despesa= Pontuacao.query.with_entities(func.avg(Pontuacao.despesa)).filter(Pontuacao.rodada==rodada_id)[0][0]
    
    rodada_atual = db.session.merge(session['rodada_atual'])
    titulo="Veja sua pontuacao da rodada"
    log=""
    if candidato_id is not None and candidato_id<>"all":
        candidato = politicaServices.pontuacaoByCandidato(candidato_id, rodada_id)
        nome_politico = Candidatura.query.filter_by(id=candidato_id).first()
        #log = log + enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada,rodada_atual,enviar, nome_politico) #politicos,
        enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada,rodada_atual,enviar, nome_politico, politicos_pontos,
                                  politicos_presenca, politicos_votacao, politicos_proposicao, politicos_despesa,
                                  media_presenca, media_votacao, media_proposicao, media_despesa)
        total = 0
        total = total +1
        log = log + ", " + str(nome_politico.email) #+ str(p[0]) 
        #return render_template("comunicado/politicoultimarodada.html",candidato, dominio=dominio,rodada=rodada,
         #                      rodada_atual=rodada_atual, nome_politico=nome_politico) #,politicos=politicos rodadaPontos=rodadaPontos,
    else:
        candidatos = Candidatura.query.first()
        total=0
        for politico in candidatos:
            candidato = politicaServices.pontuacaoByCandidato(candidato=politico.id, rodada_numero=rodada_id)
            nome_politico = Candidatura.query.filter_by(id=politico.id).first()
            total=total+1
            #log = log + enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada,politicos,rodada_atual,enviar)
            try:
                enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada,rodada_atual,enviar, nome_politico, politicos_pontos,
                                  politicos_presenca, politicos_votacao, politicos_proposicao, politicos_despesa,
                                  media_presenca, media_votacao, media_proposicao, media_despesa)
            except:
                print "Email Error"
            log = log + ", " + str(nome_politico.email)
    return render_template("comunicado/statuscomunicado.html",dominio="",titulo=titulo,total=total,log=log) 

def enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada, rodada_atual,enviar, nome_politico, politicos_pontos,
                              politicos_presenca, politicos_votacao, politicos_proposicao, politicos_despesa,
                              media_presenca, media_votacao, media_proposicao, media_despesa):
    
    log=""
    if candidato is not None: # and candidato.email is not None:
        
        #log=log+"\n"+str(time.user.email)+ " - "+str(time.id)+" - "+str(time.nome)
        #rodadaPontos=politicaServices.rodadaPontosByTime(candidato.id,rodada_id)
        #politicaServices.pontuacaoByCandidato(candidato, rodada_id)
        if enviar == 'True':
            send_mail(titulo,['danieln.silva@yahoo.com.br'],  
                       render_template("comunicado/politicoultimarodada.html",
                                       candidato=candidato,rodada=rodada,
                                      rodada_atual=rodada_atual, nome_politico=nome_politico, politicos_pontos=politicos_pontos,
                                      politicos_presenca=politicos_presenca, politicos_votacao=politicos_votacao, 
                                      politicos_proposicao=politicos_proposicao, politicos_despesa=politicos_despesa,
                                      media_presenca=media_presenca, media_votacao=media_votacao, 
                                      media_proposicao=media_proposicao, media_despesa=media_despesa)) #,politicos=politicos rodadaPontos=rodadaPontos,
#             except:
#                 print "Error EMail"
        return log + str(nome_politico.email)



@mod.route('/geral')
@mod.route('/geral/<time_id>')
def geral(time_id=None):
    #http://localhost:8084/comunicado/geral/14?comunicado=convidelink&enviar=false
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='false' #True
   
    comunicado = request.args.get('comunicado')
    if comunicado is None:
        comunicado='geral'
    total=0
    
    dominio=""
    #dominio="http://localhost:8084"
    
    titulo="Comunicado geral aos jogadores"
    log=""
    if time_id is not None and time_id<>"all":
        time = politicaServices.verTime(id=time_id)
        if time is not None and time.user is not None:
            if enviar == "True":
                print "enviando para "+time.user.email
                send_mail(titulo,[time.user.email], render_template("comunicado/"+comunicado+".html",time=time))
            
            return render_template("comunicado/"+comunicado+".html",time=time)
    else:
        times = Time.query.all()
        total=0
        for time in times:
            total=total+1
            
            if time is not None and time.user is not None:
                if enviar == "True":       
                    try: 
                        print "email:"+time.user.email
                        send_mail(titulo,[time.user.email], render_template("comunicado/"+comunicado+".html",time=time))
                    except:
                        print "Unexpected error:"         
                    
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 



@mod.route('/liganovomembro') # Daniel
@mod.route('/liganovomembro/<time_id>')
def liganovomembro(time_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='false'
   
    total=0
    
    dominio=""
    #dominio="http://localhost:8084"
    
    titulo="Novo membro na sua liga!"
    log=""
    htmlemail=None
    if time_id is not None and time_id<>"all":
        ligamembros = politicaServices.ligamembros(time=time_id)
        if ligamembros is not None:
            for ligamembro in ligamembros:                
                htmlemail=envioLigaNovoMembro(ligamembro,titulo,enviar)
            
            return envioLigaNovoMembro(ligamembro,titulo,enviar)
    else:
        ligamembros = politicaServices.ligamembros()
        total=0
        for ligamembro in ligamembros:
            total=total+1
            if enviar == "True":
                envioLigaNovoMembro(ligamembro,titulo,enviar)
                    
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 

def envioLigaNovoMembro(ligamembro,titulo,enviar):
    if enviar is None:
        enviar="True"
    timenovo = ligamembro[1]
    emailnovo = ligamembro[2]
    
    timedono = ligamembro[3]
    emaildono = str(ligamembro[4])
    
    nomeliga = ligamembro[0]
    htmlemail=render_template("comunicado/liganovomembro.html",timenovo=timenovo,emailnovo=emailnovo,timedono=timedono,emaildono=emaildono,nomeliga=nomeliga)
    if ligamembro is not None and emaildono<>emailnovo:
        
        try:  
            if enviar == "True":                  
                send_mail(titulo,[emaildono], htmlemail)             
            
        except:
            print "Error EMail"       
    return htmlemail


@mod.route('/ligapontos') # Daniel
@mod.route('/ligapontos/<time_id>')
def ligapontos(time_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='false'
   
    total=0
    
    dominio=""
    #dominio="http://localhost:8084"
    
    titulo="Acompanha suas ligas!"
    #timesInLigas
    log=""
    htmlemail=None
    if time_id is not None and time_id<>"all":
        ligamembros = politicaServices.ligamembrosPontos(time=time_id)
        if ligamembros is not None:
            for ligamembro in ligamembros:                
                htmlemail=envioLigaPontos(ligamembro,titulo,enviar)
            
            return envioLigaPontos(ligamembro,titulo,enviar)
    else:
        politicaServices.timesInLigas
        
        total=0
        for ligamembro in ligamembros:
            total=total+1
            if enviar == "True":
                envioLigaPontos(ligamembro,titulo,enviar)
                    
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 

def envioLigaPontos(ligamembro,titulo,enviar): # Daniel
    ligamembros = politicaServices.ligamembrosPontos()
    if enviar is None:
        enviar="True"
    timenovo = ligamembro[1]
    emailnovo = ligamembro[2]
    
    timedono = ligamembro[3]
    emaildono = str(ligamembro[4])
    
    nomeliga = ligamembro[0]
    htmlemail=render_template("comunicado/liganovomembro.html",timenovo=timenovo,emailnovo=emailnovo,timedono=timedono,emaildono=emaildono,nomeliga=nomeliga)
    if ligamembro is not None and emaildono<>emailnovo:
        
        try:  
            if enviar == "True":                  
                send_mail(titulo,[emaildono], htmlemail)             
            
        except:
            print "Error EMail"       
    return htmlemail