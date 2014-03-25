from sqlalchemy import func, distinct
from flask import Blueprint, request, render_template, g,flash, Response, make_response, send_file, jsonify, session, redirect, url_for


from pecbrasil import db
from pecbrasil.politica.models import Candidatura, Pontuacao,Time,Rodada,RodadaPontos
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
    form=ConvidarForm()
    if form.validate_on_submit():
        time = politicaServices.meuTime(g.user.id)
    
        send_mail(titulo,[form.email.data],   render_template("comunicado/convideamigos.html",form=form,time=time,obs=form.obs.data))
    
        return render_template("comunicado/retornarpublico.html",titulo=titulo) 
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
    rodada_id=rodada.id
    total=0
    
    politicos=politicaServices.topPoliticosRodada(tamanho=5)
    
    titulo="Veja sua pontuacao da rodada"
    log=""
    if time_id is not None:
        time = politicaServices.meuTime(time_id)
        
        if time is not None:
            if enviar == 'True':
                send_mail(titulo,[time.user.email],   
                          render_template("comunicado/ultimarodada.html",time=time,rodada=rodada,pontos=pontos,politicos=politicos))
            total=total+1
            log=log+"\n"+time.user.email+ " - "+str(time.id)+" - "+time.nome
            rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
            return render_template("comunicado/ultimarodada.html",time=time,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos)
    else:
        times = Time.query.all()
        for time in times:
            if time is not None:
                total=total+1
                log=log+"\n"+time.user.email+ " - "+str(time.id)+" - "+time.nome
                rodadaPontos=politicaServices.rodadaPontosByTime(time.id,rodada_id)
                if enviar == 'True':
                    send_mail(titulo,[time.user.email],  
                              render_template("comunicado/ultimarodada.html",time=time,rodada=rodada,rodadaPontos=rodadaPontos,politicos=politicos))
    
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
            send_mail(titulo,[time.user.email],   render_template("comunicado/criartime.html",time=time))
            total=total+1
            log=log+","+time.user.email
    else:
        db.session.execute("select email, nickname, fullname from account_user where id not in (select user_id from time)")
        rows = db.session.fetchall()
        total=0
        for row in rows:
            send_mail(titulo,[row[0]],  render_template("comunicado/criartime.html",email=row[0],nickname=row[1],fullname=row[2]))
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
            send_mail(titulo,time.user.email,   render_template("comunicado/retornar.html",time=time))
            total=total+1
            log=log+","+time.user.email
    else:
        db.session.execute("select email, nickname, fullname from account_user where last_seen < date_sub(now(), interval 1 month)")
        rows = db.session.fetchall()
        total=0
        for row in rows:
            send_mail(titulo,row[0],  render_template("comunicado/retornar.html",email=row[0],nickname=row[1],fullname=row[2]))
            total=total+1
            log=log+","+time.user.email
<<<<<<< HEAD
                    
=======
<<<<<<< HEAD
                    
=======
                    
>>>>>>> 4c1441279a5877441451f62dfbfb52a0f675e27f
>>>>>>> 1e56bce78ac59d9c18e2c711be8545a053dc5a8d
    return render_template("comunicado/statuscomunicado.html",titulo=titulo,total=total,log=log)    