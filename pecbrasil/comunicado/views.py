from sqlalchemy import func, distinct
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for
from datetime import datetime

from pecbrasil import db
from pecbrasil.politica.models import Candidatura, Pontuacao,Time,Rodada,RodadaPontos
from pecbrasil.liga.models import Convite
from pecbrasil.utils import exist_or_404, gzip_data, cached_query
from pecbrasil.politica.services import PoliticaServices
from pecbrasil.comunicado.forms import ConvidarForm
from flask.ext.mail import Message
from config import ADMINS
from pecbrasil import mail
from pecbrasil.utils import send_mail

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
                print send_mail(titulo,[email],   render_template("comunicado/convideamigos.html",form=form,time=time,obs=form.obs.data))
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
    titulo="Veja sua pontuacao da rodada"
    log=""
    if time_id is not None and time_id<>"all":
        time = politicaServices.verTime(id=time_id)
        if time is not None:
            log = log + enviaUltimaRodada(time,rodada_id,titulo,rodada,politicos,rodada_atual,enviar)
            rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
            return render_template("comunicado/ultimarodada.html",dominio=dominio,time=time,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos,rodada_atual=rodada_atual)
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
                      render_template("comunicado/ultimarodada.html",time=time,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos,rodada_atual=rodada_atual))
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
                    send_mail(titulo,[time.user.email],  render_template("comunicado/timeincompleto.html",time=time))
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
            send_mail(titulo,[time.user.email],   render_template("comunicado/abrecampeonato.html",time=time))
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
              
    
    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)   


@mod.route('/criartime/')
@mod.route('/criartime/<time_id>')
def criartime(time_id=None): 
    titulo="Crie seu time"
    total=0
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        if time is not None:
            try:
                send_mail(titulo,[time.user.email],   render_template("comunicado/criartime.html",time=time))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email
    else:
        db.session.execute("select email, nickname, fullname from account_user where id not in (select user_id from time)")
        rows = db.session.fetchall()
        total=0
        for row in rows:
            try:
                send_mail(titulo,[row[0]],  render_template("comunicado/criartime.html",email=row[0],nickname=row[1],fullname=row[2]))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email
                
    
    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)    


@mod.route('/retornar/')
@mod.route('/retornar/<time_id>')
def retornar(time_id=None): 
    titulo="Faz tempo que nao joga, vamos voltar?"
    total=0
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        if time is not None:
            try:
                send_mail(titulo,time.user.email,   render_template("comunicado/retornar.html",time=time))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email
    else:
        db.session.execute("select email, nickname, fullname from account_user where last_seen < date_sub(now(), interval 1 month)")
        rows = db.session.fetchall()
        total=0
        for row in rows:
            try:
                send_mail(titulo,row[0],  render_template("comunicado/retornar.html",email=row[0],nickname=row[1],fullname=row[2]))
            except:
                    print "Unexpected error:"
                    print "Error EMail"
            total=total+1
            log=log+","+time.user.email

    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)   


@mod.route('/politicoultimarodada')
@mod.route('/politicoultimarodada/<rodada_id>')
@mod.route('/politicoultimarodada/<rodada_id>/<time_id>')
def politicoultimarodada(rodada_id=None,time_id=None):
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
    titulo="Veja sua pontuacao da rodada"
    log=""
    if time_id is not None and time_id<>"all":
        time = politicaServices.verTime(id=time_id)
        if time is not None:
            log = log + enviaPoliticoUltimaRodada(time,rodada_id,titulo,rodada,politicos,rodada_atual,enviar)
            rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
            return render_template("comunicado/politicoultimarodada.html",dominio=dominio,time=time,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos,rodada_atual=rodada_atual)
    else:
        candidatos = Candidatura.query.all()
        total=0
        for candidato in candidatos:
            total=total+1
            log = log + enviaPoliticoUltimaRodada(time,rodada_id,titulo,rodada,politicos,rodada_atual,enviar)
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 

def enviaPoliticoUltimaRodada(candidato,rodada_id,titulo,rodada,politicos,rodada_atual,enviar):
    
    log=""
    if candidato is not None and candidato.email is not None:
        
        #log=log+"\n"+str(time.user.email)+ " - "+str(time.id)+" - "+str(time.nome)
        rodadaPontos=politicaServices.rodadaPontosByTime(candidato.id,rodada_id)
        if enviar == 'True':
            try:
                send_mail(titulo,[candidato.email],  
                      render_template("comunicado/politicoultimarodada.html",candidato=candidato,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos,rodada_atual=rodada_atual))
            except:
                    print "Error EMail"
    return log  



@mod.route('/geral')
@mod.route('/geral/<time_id>')
def geral(time_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='True'
   
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
                send_mail(titulo,[time.user.email], render_template("comunicado/geral.html",time=time))
            
            return render_template("comunicado/geral.html",time=time)
    else:
        times = Time.query.all()
        total=0
        for time in times:
            total=total+1
            print "olaa:"+str(time.user.email)
            if time is not None and time.user is not None:
                if enviar == "True":       
                    try: 
                        print "email:"+time.user.email
                        send_mail(titulo,[time.user.email], render_template("comunicado/geral.html",time=time))
                    except:
                        print "Unexpected error:"         
                    
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 



@mod.route('/liganovomembro')
@mod.route('/liganovomembro/<time_id>')
def liganovomembro(time_id=None):
    enviar = request.args.get('enviar')
    if enviar is None:
        enviar='true'
   
    total=0
    
    dominio=""
    #dominio="http://localhost:8084"
    
    titulo="Novo membro na sua liga!"
    log=""
    if time_id is not None and time_id<>"all":
        ligamembros = politicaServices.ligamembros()
        time = politicaServices.verTime(id=time_id)
        if time is not None and time.user is not None:
            if enviar == "True":
                print "enviando para "+time.user.email
                envioLigaNovoMembro(ligamembro,titulo)
            
            return render_template("comunicado/liganovomembro.html",time=time)
    else:
        ligamembros = politicaServices.ligamembros()
        times = Time.query.all()
        total=0
        for ligamembro in ligamembros:
            total=total+1
            envioLigaNovoMembro(ligamembro,titulo)
                    
    return render_template("comunicado/statuscomunicado.html",dominio=dominio,titulo=titulo,total=total,log=log) 

def envioLigaNovoMembro(ligamembro,titulo):
                
    timenovo = ligamembro[1]
    emailnovo = ligamembro[2]
    
    timedono = ligamembro[3]
    emaildono = str(ligamembro[4])
    
    nomeliga = ligamembro[0]
    
    if ligamembro is not None and emaildono<>emailnovo:
        
        try:                
            print "#################:"+nomeliga
            print timenovo+emailnovo
            print timedono+emaildono
        
            if enviar == "True":  
                send_mail(titulo,[emaildono], render_template("comunicado/liganovomembro.html",timenovo=timenovo,emailnovo=emailnovo,timedono=timedono,emaildono=emaildono,nomeliga=nomeliga))
             
            
        except:
            print "Error EMail"       
