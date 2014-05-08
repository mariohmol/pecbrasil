# -*- coding: utf-8 -*- 
from pecbrasil.politica.models import Candidatura, Pontuacao,Partido,Time,RodadaPontos,TimeCandidato
from pecbrasil.liga.models import Liga,LigaJogador
from pecbrasil.proposicao.models import Proposicao,TimeVotacao,VotacaoCandidato,Repasse,StatusProposicao,TipoProposicao,ProposicaoAcao
from pecbrasil.politica.models import Rodada,Politico,ProcessoCandidato,DespesaCandidato
from pecbrasil.orgao.models import Orgao
from pecbrasil.utils import clean_varrequest

from flask import session
from pecbrasil import db
from string import upper

class PoliticaServices(object):
    
    
    ###########################
    # TIME
    ###########################
    
    #dados do time + lista de politicos
    def verTime(self,nome=None,id=None):        
        if nome is not None:
            times = Time.query.filter_by(nome=nome).outerjoin(TimeCandidato).order_by(TimeCandidato.posicao).join(Candidatura).first() 
                        
        elif id is not None:
            times = Time.query.filter_by(id=id).outerjoin(TimeCandidato).outerjoin(Candidatura).first() 
        else:
            times = Time.query.outerjoin(TimeCandidato).outerjoin(Candidatura).order_by(Time.pontuacao_total.desc()).all()
        return times

    def meuTime(self,userId=None): 
        return Time.query.filter_by(user_id=userId).outerjoin(TimeCandidato).order_by(TimeCandidato.posicao.asc()).outerjoin(Candidatura).first()  
    
    def meusCandidatos(self,userId=None): 
        return TimeCandidato.query.filter_by(user_id=userId).join(Time).order_by(TimeCandidato.posicao.asc()).join(Candidatura).first()  
 
    def timesFaltandoPolitico(self):
        return db.session.execute("select * from time where (select count(*) from timecandidato tc where tc.time=time.id)<4")
            
    def top3Time(self):  
        return Time.query.order_by(Time.pontuacao_total.desc()).limit(3)
    
    def topTimes(self):        
        return Time.query.order_by(Time.pontuacao_total.desc()).all()
  
    def timesInLigas(self):
        return db.session.execute("SELECT * FROM time where id in (select distinct user_ligajogador from ligajogador) ")
  
    ###########################
    # POLITICOS
    ###########################
    
      
    def verCandidatura(self,nome=None,order=None,orderdirec=None,estado=None): 
        nome=clean_varrequest(nome)
        estado=clean_varrequest(estado)
        order=clean_varrequest(order,"pontuacao_total")
        orderdirec=clean_varrequest(orderdirec,"desc")
    
        politicos=None
        
        if order and orderdirec:
            order="candidatura."+order+ " "+ orderdirec  
        elif order:    
            order="candidatura."+order+ " desc" 
          
        if nome is None or nome == "all":
            politicos = Candidatura.query
           
                
            #all()        
        elif not nome.isdigit():
            nomeT='%'+nome+'%'
            politicos = Candidatura.query.outerjoin(Politico).filter(Politico.nome.ilike(nomeT))\
            .outerjoin(Partido)
        elif nome.isdigit():   
            politicos = Candidatura.query.outerjoin(Politico).filter(Candidatura.id==nome).outerjoin(Partido) 
        #filter(User.name.like('%ed%')).\\
        if estado is not None and estado <> 'all':
            estado=upper(estado)
            politicos = politicos.filter(Candidatura.uf==estado) 
            
        if order:
            politicos = politicos.order_by(order).limit(200).all()
        else:
            politicos = politicos.order_by(Candidatura.pontuacao_total.desc()).limit(200).all() 
            #if politicos is None or len(politicos)==0 :
            #    politicos = Candidatura.query\
            #    .join(Politico).join(Partido)\
            #    .filter(Candidatura.politico==nome).order_by(Candidatura.pontuacao_total.desc()).first()
        
        if politicos is None:
            politicos = Candidatura.query.join(Politico)\
            .filter(Candidatura.id==nome)
            
            if order:
                politicos = politicos.order_by(order).first()
            else:
                politicos = politicos.order_by(Candidatura.pontuacao_total.desc()).first()
                
            #.join(Partido)
            #politicos=4
         
        return politicos
    
      
    def topPoliticos(self,nome=None):  
        if nome is not None:
            politicos = Candidatura.query.filter_by(nome=nome).order_by(Candidatura.pontuacao_total.desc()).first()
        else:
            # politicos = Candidatura.query.join(Candidatura.politico).order_by(Candidatura.pontuacaoTotal).all()
            #politicos = Politico.query.join(Politico.candidaturas).order_by(Candidatura.pontuacaoTotal).all()
            politicos = db.session.query(Candidatura,Politico).filter(Candidatura.politico == Politico.id)\
            .order_by(Candidatura.pontuacao_total.desc()).all()
        return politicos
    
    def topPoliticosRodada(self,partido=None,tamanho=None):  
        if tamanho is None:
            tamanho=1
        if partido is not None:
            politicos = Candidatura.query.filter_by(partido=partido).order_by(Candidatura.pontuacao_ultima.desc()).limit(tamanho)
        else:
            # politicos = Candidatura.query.join(Candidatura.politico).order_by(Candidatura.pontuacaoTotal).all()
            #politicos = Politico.query.join(Politico.candidaturas).order_by(Candidatura.pontuacaoTotal).all()
            politicos = db.session.query(Candidatura,Politico).filter(Candidatura.politico == Politico.id)\
            .order_by(Candidatura.pontuacao_ultima.desc()).limit(tamanho)
        return politicos
    
    def pontoByPolitico(self,nome=None):  
        if nome is not None:
            politicos = RodadaPontos.query.filter_by(time=nome).order_by(RodadaPontos.rodada).all()
        else:
            politicos = db.session.query(RodadaPontos,Time).filter(RodadaPontos.time == Time.id).order_by(RodadaPontos.rodada).all()
        return politicos

  
    def candidaturaByPartido(self,partidoSigla=None,offset=None,limit=None):        
        if partidoSigla is None:
            politicos = Candidatura.query.order_by(Candidatura.pontuacao_total).limit(limit).offset(offset).all()        
        else:
            politicos = Candidatura.query.join(Partido).filter(Partido.sigla==partidoSigla).order_by(Candidatura.pontuacao_total.desc()).limit(limit).offset(offset).all()
            if politicos is None or len(politicos)==0:
                politicos = Candidatura.query.join(Partido).filter(Partido.id==partidoSigla).order_by(Candidatura.pontuacao_total.desc()).limit(limit).offset(offset).all()
        return politicos

   
    ###########################
    # PARTIDO
    ###########################
    
      
    def partidosPopulares(self,name=None):        
        if name is not None:
            politicos = Partido.query.first()
        else:
            politicos = Partido.query.all()
        return politicos
 
 
    ###########################
    # PONTOS
    ###########################  
    
    def pontoTimes(self,nome=None):  
        if nome is not None:
            politicos = db.session.query(Rodada,RodadaPontos).filter_by(Rodada.id==nome).order_by(Pontuacao.rodada,RodadaPontos.pontos.desc()).all()
        else:
            politicos = db.session.query(Rodada,RodadaPontos).filter(Pontuacao.candidatura == Politico.id).order_by(Pontuacao.rodada,RodadaPontos.pontos.desc()).all()
        return politicos
    
    def rodadaPontosByTime(self,time_id=None,rodada_id=None):
        rodadaPontos= RodadaPontos.query.filter(RodadaPontos.time==time_id,RodadaPontos.rodada==rodada_id).first()
        return rodadaPontos
                   
    def pontoPoliticoRodada(self,nome=None): 
        if nome is not None:
            politicos = Pontuacao.query.join(Rodada).filter(Rodada.id==nome).join(Candidatura).order_by(Rodada.inicio,Pontuacao.pontos.desc()).all()
        else:
            politicos = db.session.query(Rodada,Pontuacao).filter(Rodada.id == Pontuacao.rodada).order_by(Rodada.inicio,Pontuacao.pontos.desc()).all()
        return politicos    
    
    def pontoRodada(self,nome=None):  
        if nome is not None:
            politicos = db.session.query(Rodada,RodadaPontos).filter(Rodada.id == RodadaPontos.rodada,Rodada.id==nome).order_by(Rodada.inicio,RodadaPontos.pontos.desc()).all()
        else:
            politicos = db.session.query(Rodada,RodadaPontos).filter(Rodada.id == RodadaPontos.rodada).order_by(Rodada.id,RodadaPontos.pontos.desc()).all()
        return politicos
    
      
    def pontuacaoByPartido(self,partidoSigla=None):        
        if partidoSigla is None:
            politicos = Pontuacao.query.filter_by(ativo=1).order_by(Pontuacao.rodada).all()        
        else:
            politicos = Pontuacao.query.filter_by(ativo=1).join(Candidatura).join(Partido)\
            .filter(Partido.sigla==partidoSigla).order_by(Pontuacao.rodada).all()
            if politicos is None or len(politicos)==0:
                politicos = Pontuacao.query.join(Candidatura).join(Partido)\
            .filter(Partido.id==partidoSigla).order_by(Pontuacao.rodada).all()
        return politicos
    
    def pontuacaoSumRodadaByPartido(self,candidatura_id=None,partidoSigla=None):        
        
        sql="SELECT max(p.rodada) as rodada, sum(p.candidatura) as candidatura, sum(p.pontos) as pontos    ,        \
            sum(p.presenca) as presenca, avg(p.tendencia_presenca) as tendencia_presenca, max(p.total_presenca) as total_presenca, \
            sum(p.proposicao) as proposicao, avg(p.tendencia_proposicao) as tendencia_proposicao, max(p.total_proposicao) as total_proposicao, \
            sum(p.processo) as processo, avg(p.tendencia_processo) as tendencia_processo, max(p.total_processo) as total_processo, \
            sum(p.votacao) as votacao, avg(p.tendencia_votacao) as tendencia_votacao, max(p.total_votacao) as total_votacao, \
            sum(p.despesa) as despesa, avg(p.tendencia_despesa) as tendencia_despesa, max(p.total_despesa) as total_despesa  \
            FROM pontuacao p,candidatura c where p.candidatura=c.id AND p.ativo=1 "

        if partidoSigla is not None:
            sql +=" AND  candidatura.partido="+partidoSigla
        if candidatura_id is not None:
            sql +=" AND  candidatura.id="+candidatura_id
        
            
        sql +=" group by p.candidatura"
        politicos = db.session.execute(sql)
        #politicos = db.session.query(sql)
        return politicos
    
 
 

  
    ###########################
    # RODADAS
    ###########################
      
    def rodadas(self,nome=None):
        if nome is not None:
            rodadas = Rodada.query.filter_by(id=nome).first()        
        else:
            rodadas = Rodada.query.filter_by(ativo=1).order_by(Rodada.ano.desc(),Rodada.semana.desc()).all()
        return rodadas
    
    def rodadaAtual(self,nome=None):  
        if nome is not None:
            politicos = Rodada.query.filter_by(ativo=1,semana=nome).order_by(Rodada.id.desc()).first()
        else:
            politicos = Rodada.query.filter_by(ativo=1).order_by(Rodada.id.desc()).first()
        return politicos
  
    def getRodada(self,rodada_id=None):
        if rodada_id is None or rodada_id == "all":
            rodada = self.rodadaAtual()
        else:
            rodada = Rodada.query.filter(Rodada.id==rodada_id).first()
        return rodada

    def proximaRodada(self,rodada_id=None,inicio=None):
        return Rodada.query.filter(Rodada.inicio>inicio).order_by(Rodada.ano.asc(),Rodada.semana.asc()).first()
        
    def anteriorRodada(self,rodada_id=None,inicio=None):
         return Rodada.query.filter(Rodada.inicio<inicio).order_by(Rodada.ano.desc(),Rodada.semana.desc()).first()  
     
    ###########################
    # PROPOSICAO
    ###########################         
    def proposicaoCompleta(self,id=None):
        ret = Proposicao.query.filter_by(id=proposicao_id).outerjoin(Candidatura).outerjoin(StatusProposicao)
        ret = ret.outerjoin(TipoProposicao).first()
        
         
    def proposicao(self,candidatura_id=None,partido_sigla=None):
        ret = None
        if candidatura_id == 'all' and partido_sigla is not None:
            ret = Proposicao.query.outerjoin(Candidatura).filter_by(partido=partido_sigla).outerjoin(StatusProposicao).outerjoin(TipoProposicao).all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = Proposicao.query.all()
        elif candidatura_id is not None and (partido_sigla is None or partido_sigla=="all"):
            ret = Proposicao.query.outerjoin(Candidatura).filter_by(id=candidatura_id).outerjoin(StatusProposicao).outerjoin(TipoProposicao).all()
        else:
            ret = Proposicao.query.all()
        return ret
    
    def proposicaoacao(self,dataInicio,proposicao_id=None,candidatura_id=None,partido_sigla=None):
        ret = ProposicaoAcao.query
        if dataInicio:
            ret=ret.filter_by(data_proposicaoacao=dataInicio)
            
        ret = ret.outerjoin(Proposicao).outerjoin(StatusProposicao)
        
        
        if proposicao_id is not None and proposicao_id <> 'all':
            ret = ret.filter(ProposicaoAcao.proposicao_proposicaoacao==proposicao_id).all()
        elif candidatura_id == 'all' and partido_sigla is not None:
            ret = ret.outerjoin(Candidatura).filter_by(partido=partido_sigla).outerjoin(StatusProposicao).outerjoin(TipoProposicao).all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = ret.all()
        elif candidatura_id is not None and (partido_sigla is None or partido_sigla=="all"):
            ret = ret.outerjoin(Candidatura).filter_by(id=candidatura_id).outerjoin(StatusProposicao).outerjoin(TipoProposicao).all()
        else:
            ret = ret.all()
        return ret
    
    def ultimasProposicaoacao(self):
        ret = ProposicaoAcao.query.outerjoin(Proposicao).outerjoin(StatusProposicao)
        ret=ret.order_by(ProposicaoAcao.data_proposicaoacao.desc()).limit(10).all()
        return ret

    def ultimasProposicaovotacao(self,total=10):
        ret = Proposicao.query.outerjoin(TipoProposicao).outerjoin(StatusProposicao)
        ret=ret.filter(Proposicao.datavotacao!=None).order_by(Proposicao.datavotacao.desc()).limit(total).all()
        return ret
                           
    def atualizaTipoVotacaoProposicao(self):
        sql="update tipoproposicao set votacao_tipoproposicao=1 where id_tipoproposicao in ( select distinct tipo from proposicao where id in (SELECT proposicao FROM `votacaocandidato`) )"
        db.session.execute(sql)
        sql="update tipoproposicao set votacao_tipoproposicao=1 where id_tipoproposicao in (SELECT tipo FROM `proposicao` where datavotacao is not null)"
        db.session.execute(sql)
        db.session.commit()
    
    
    ##########################
    #
    # LIGAS
    ##########################
        
    def liga(self,liga_id=None,nome=None):
        if liga_id is not None:
            return Liga.query.filter_by(id_liga=liga_id).first()
        elif nome is not None:
            return Liga.query.filter_by(nome_liga=nome).first()
        
     
    def ligamembrosPontos(self,time=None):
        query =  "SELECT user_ligajogador, id_liga, nome_liga, posicaoanterior, posicao, pontos_ligajogador"
        query = query + "FROM ligajogador, liga WHERE  "+ time +" = user_ligajogador"
        query = query + "AND id_liga = liga_ligajogador"
        return db.session.execute(query)
        
   
    def ligamembros(self,liga_id=None,time=None,dataentrada=None):
        #if liga_id is not None:
        #     ret = LigaJogador.query.filter_by(id_liga=liga_id)
        #elif nome is not None:
        #    ret= LigaJogador.query.filter_by(nome_liga=nome)
        #else:
        #    ret=  LigaJogador.query
        #ret=ret.outerjoin((Liga,LigaJogador.liga_ligajogador==Liga.id_liga))
        #ret=ret.outerjoin((Time,Liga.criador_liga==Time.id))
        #ret=ret.outerjoin((Time,Liga.criador_liga==Time.id))
        #if dataentrada is not None:
        #    ret=ret.filter_by(data_ligajogador>=dataentrada)

        query = "SELECT liga.nome_liga,timejogador.nome , userjogador.email, timedono.nome, userdono.email  "
        query = query + " FROM ligajogador, liga, " 
        query = query + "time as timejogador, time as timedono, "
        query = query + "account_user as userjogador, account_user userdono where "
        query = query + "liga.id_liga=ligajogador.liga_ligajogador and "
        query = query + "ligajogador.user_ligajogador=timejogador.id and timedono.id = liga.criador_liga and " 
        query = query + "userjogador.id = timejogador.user_id and userdono.id = timedono.user_id "
        if dataentrada is not None:
            query = query + " AND ligajogador.data_ligajogador>="+dataentrada
        if time is not None:
            query = query + " AND timedono.id="+time

        return db.session.execute(query)
        #return ret.all()  
    

    ###########################
    # LIST TABELAS EM GERAL
    ###########################
      
         
    def votacaoCandidatura(self,candidatura_id=None,partido_sigla=None):
        ret = None
        if candidatura_id is None:
            ret = VotacaoCandidato.query.join(Proposicao).all()
        elif candidatura_id == 'all' and partido_sigla is not None:
            ret = VotacaoCandidato.query.join(Proposicao).all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = VotacaoCandidato.query.join(Proposicao).all()
        else:
            ret = VotacaoCandidato.query.filter_by(candidatura=candidatura_id).join(Proposicao).all()
        return ret
    
    def processocandidato(self,candidatura_id=None,partido_sigla=None):
        ret = None
        if candidatura_id is None:
            ret = ProcessoCandidato.query.all()
        elif candidatura_id == 'all' and partido_sigla is not None:
            ret = ProcessoCandidato.query.all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = ProcessoCandidato.query.all()
        else:
            ret = ProcessoCandidato.query.filter_by(candidatura=candidatura_id).all()
        return ret
    
    def despesacandidato(self,candidatura_id=None,partido_sigla=None):
        ret = None
        #print 'ola'
        if candidatura_id is None:
            ret = DespesaCandidato.query.join(Rodada).filter_by(ativo=1)\
            .order_by(Rodada.inicio.desc()).all()
        elif candidatura_id == 'all' and partido_sigla is not None:
            ret = DespesaCandidato.query.join(Rodada).filter_by(ativo=1)\
            .order_by(Rodada.inicio.desc()).all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = DespesaCandidato.query.join(Rodada).filter_by(ativo=1)\
            .order_by(Rodada.inicio.desc()).all()
        else:
            ret = DespesaCandidato.query.filter_by(candidatura=candidatura_id).join(Rodada)\
            .filter_by(ativo=1).order_by(Rodada.inicio.desc()).all()
        return ret
 
    def despesaByTipo(self,despesatipo_id=None):
        ret = None
        #print 'ola'
        if despesatipo_id is None:
            ret = DespesaCandidato.query.join(Rodada).order_by(Rodada.inicio).all()
        else:
            ret = DespesaCandidato.query.filter_by(categoria=despesatipo_id).join(Rodada)\
            .order_by(Rodada.inicio).all()
        return ret

 
         
    def orgao(self,candidatura_id=None,partido_sigla=None):
        ret = None
        if candidatura_id == 'all' and partido_sigla is not None:
            ret = Orgao.query.join(Candidatura).filter_by(partido=partido_sigla).all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = Orgao.query.all()
        elif candidatura_id is not None and (partido_sigla is None or partido_sigla=="all"):
            ret = Orgao.query.filter_by(candidatura=candidatura_id).all()
        else:
            ret = Orgao.query.all()
        return ret
    
    
    def votacao(self,proposicao_id=None,candidatura_id=None):
        ret = None
        if (candidatura_id == 'all' or candidatura_id is None) and proposicao_id is not None:
            ret = VotacaoCandidato.query.filter_by(proposicao=proposicao_id).join(Candidatura) #.join(Candidatura)
        elif candidatura_id == 'all' and proposicao_id is None:
            ret = VotacaoCandidato.query.join(Candidatura)
        elif candidatura_id is not None and (proposicao_id is None or proposicao_id=="all"):
            ret = VotacaoCandidato.query.filter_by(candidatura=candidatura_id)
        else:
            ret = VotacaoCandidato.query.join(Candidatura)
        ret=ret.join(Partido).order_by(Partido.sigla,Candidatura.name_pt).all()
        return ret
    
    def repasse(self,candidatura_id=None,partido_sigla=None):
        ret = None
        if candidatura_id is None:
            ret = VotacaoCandidato.query.all()
        elif candidatura_id == 'all' and partido_sigla is not None:
            ret = VotacaoCandidato.query.all()
            #ret = candidaturaByPartido(partido_sigla) 
        elif candidatura_id == 'all' and partido_sigla is None:
            ret = VotacaoCandidato.query.all()
        else:
            ret = VotacaoCandidato.query.filter_by(id=candidatura_id).all()
        return ret

#############################################
### SCRIPTS DO IMPORT
        
    def updatePontuacaoCandidatosSQL(self,anoatual):    
        db.session.execute("update candidatura c set c.pontuacao_total = (SELECT sum(p.pontos) FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        
        db.session.execute("update candidatura c set c.pontuacao_ultima = (SELECT p.pontos FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and  p.candidatura = c.id order by p.rodada desc limit 1  )")
        
        #db.session.execute("update candidatura c set c.pontuacao_tendencia = (SELECT avg(pontos)/c.pontuacao_ultima FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and p.candidatura = c.id group by p.candidatura )")
        
        db.session.execute("update candidatura c set c.total_votacao = (SELECT total_votacao FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        db.session.execute("update candidatura c set c.total_presenca = (SELECT total_presenca FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        db.session.execute("update candidatura c set c.total_processo = (SELECT total_processo FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        db.session.execute("update candidatura c set c.total_proposicao = (SELECT total_proposicao FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        db.session.execute("update candidatura c set c.total_despesa = (SELECT total_despesa FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and r.ano= '"+anoatual+"' and p.candidatura = c.id group by p.candidatura )")
        db.session.execute("update pontuacao p set p.ativo=0 where rodada > (select max(r.id) from rodada r where  r.ativo =1 and r.ano= '"+anoatual+"' )")
        db.session.execute("update pontuacao p set p.ativo=1 where rodada <= (select max(r.id) from rodada r where  r.ativo =1 and r.ano= '"+anoatual+"' )")
        db.session.commit()
        return 
     
    def updatePontuacaoCandidatosTotalSQL(self,anoatual):    
        
        query="insert into candidaturatotal (candidatura,ano,partido) select id, '"+anoatual+"',partido from candidatura where id not in (select candidatura from candidaturatotal where ano='"+anoatual+"')"
        db.session.execute(query)
        db.session.execute("update candidaturatotal c set c.pontuacao_total = (SELECT sum(p.pontos) FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and p.candidatura = c.candidatura and c.ano = r.ano group by p.candidatura,r.ano )")
        
        db.session.execute("update candidaturatotal c set c.pontuacao_ultima = (SELECT p.pontos FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and  p.candidatura = c.candidatura order by p.rodada desc limit 1  )")
        
        #db.session.execute("update candidatura c set c.pontuacao_tendencia = (SELECT avg(pontos)/c.pontuacao_ultima FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and p.candidatura = c.id group by p.candidatura )")
        
        db.session.execute("update candidaturatotal c set c.total_votacao = (SELECT total_votacao FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and p.candidatura = c.candidatura group by p.candidatura )")
        db.session.execute("update candidaturatotal c set c.total_presenca = (SELECT total_presenca FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and p.candidatura = c.candidatura group by p.candidatura )")
        db.session.execute("update candidaturatotal c set c.total_processo = (SELECT total_processo FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and p.candidatura = c.candidatura group by p.candidatura )")
        db.session.execute("update candidaturatotal c set c.total_proposicao = (SELECT total_proposicao FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and p.candidatura = c.candidatura group by p.candidatura )")
        db.session.execute("update candidaturatotal c set c.total_despesa = (SELECT total_despesa FROM pontuacao p,rodada r where r.id = p.rodada and r.ativo =1 and c.ano = r.ano and p.candidatura = c.candidatura group by p.candidatura )")
        
        db.session.commit()
        return 
                           
    #rodada=rodada.getMaxRodada()
    #self.updatePontuacaoCandidatosRodados(rodada,"pontuacao_total")
    #self.updatePontuacaoCandidatosRodados(rodada-1,"pontuacao_ultima")        
    def updatePontuacaoCandidatosRodados(self,rodada,campo):    
        db.session.execute("SELECT candidatura,sum(pontos) FROM pontuacao where rodada=%s group by candidatura",[rodada])
        rows = db.session.fetchall()
        for row in rows:
            candidato=row[0]
            total=row[1]
            if campo=="pontuacao_total":
                db.session.execute("update candidatura set pontuacao_total = %s where id = %s",[total,candidato] )
            else:
                db.session.execute("update candidatura set pontuacao_ultima = %s where id = %s",[total,candidato] )
            print row[1] 
        db.session.commit()     
    
    def updatePontuacaoPartidosSQL(self):           
        sql="update partido p set "+ \
        "total_votacao = ( select sum(total_votacao) from candidatura where partido = p.id ),"+\
        "pontuacao_total_media = ( select avg(pontuacao_total) from candidatura where partido = p.id ),"+\
         "pontuacao_total = ( select sum(pontuacao_total) from candidatura where partido = p.id ),"+\
        "pontuacao_ultima = ( select sum(pontuacao_ultima) from candidatura where partido = p.id ),"+\
        "pontuacao_tendencia = ( select sum(pontuacao_tendencia) from candidatura where partido = p.id ),"+\
        "total_votacao = ( select sum(total_votacao) from candidatura where partido = p.id ),"+\
        "total_presenca = ( select sum(total_presenca) from candidatura where partido = p.id ),"+\
        "total_processo = ( select sum(total_processo) from candidatura where partido = p.id ),"+\
        "total_proposicao = ( select sum(total_proposicao) from candidatura where partido = p.id ),"+\
        "total_despesa = ( select sum(total_despesa) from candidatura where partido = p.id ),"+\
        "politico_total = ( select count(1) from candidatura where partido = p.id )"
        db.session.execute(sql)

    def updatePontuacaoPartidosTotalSQL(self,anoatual):      
        query="insert into partidototal (partido,sigla,codigo,ano) select id,sigla,codigo, '"+anoatual+"' from partido where id not in (select partido from partidototal where ano='"+anoatual+"')"
        db.session.execute(query)
        
             
        sql="update partidototal p set "+ \
        "total_votacao = ( select sum(total_votacao) from candidaturatotal where partido = p.partido and ano= '"+anoatual+"'),"+\
        "pontuacao_total_media = ( select avg(pontuacao_total) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"'),"+\
         "pontuacao_total = ( select sum(pontuacao_total) from candidaturatotal where partido = p.partido and ano= '"+anoatual+"'),"+\
        "pontuacao_ultima = ( select sum(pontuacao_ultima) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"'),"+\
        "pontuacao_tendencia = ( select sum(pontuacao_tendencia) from candidaturatotal where partido = p.partido and ano= '"+anoatual+"'),"+\
        "total_votacao = ( select sum(total_votacao) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"'),"+\
        "total_presenca = ( select sum(total_presenca) from candidaturatotal where partido = p.partido and ano= '"+anoatual+"'),"+\
        "total_processo = ( select sum(total_processo) from candidaturatotal where partido = p.partido and ano= '"+anoatual+"'),"+\
        "total_proposicao = ( select sum(total_proposicao) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"'),"+\
        "total_despesa = ( select sum(total_despesa) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"'),"+\
        "politico_total = ( select count(1) from candidaturatotal where partido = p.partido  and ano= '"+anoatual+"')"
        db.session.execute(sql)
        
                
    def updateProposicao(self):     
        sql="update proposicao p set p.favor = (select count(1) from votacaocandidato where voto=1 and p.id=proposicao)," + \
        "p.contra = (select count(1) from votacaocandidato where voto=3 and p.id=proposicao)," + \
        "p.abstencao = (select count(1) from votacaocandidato where voto=2 and p.id=proposicao)"
        db.session.execute(sql)
        db.session.commit()
        
################
# UPDATE TIMES        
################       
    def updatePontuacaoTimesSQL(self,anoatual):    
        db.session.execute("update time c set c.pontuacao_total = (SELECT sum(p.pontos) FROM rodadapontos p,rodada r where r.id = p.rodada and r.ano='"+anoatual+"' and r.ativo =1 and p.time = c.id group by p.time )")
        
        db.session.execute("update time c set c.pontuacao_ultima = (SELECT p.pontos FROM rodadapontos p,rodada r where r.id = p.rodada and r.ano='"+anoatual+"' and r.ativo =1 and  p.time = c.id order by p.rodada desc limit 1  )")
        
        db.session.execute("update time c set c.pontuacao_tendencia = (SELECT avg(pontos)/c.pontuacao_ultima FROM rodadapontos p ,rodada r where r.id = p.rodada and r.ano='"+anoatual+"' and r.ativo =1 and p.time = c.id group by p.time )")
        
        db.session.execute("update rodadapontos p set p.ativo=0 where rodada > (select max(r.id) from rodada r where  r.ativo =1)")
        
        sql="update ligajogador l set l.pontos_ligajogador= (SELECT sum(p.pontos_ligapontos) FROM ligapontos p "
        db.session.execute(sql+"  where p.time_ligapontos = l.user_ligajogador and p.liga_ligapontos = l.liga_ligajogador)")
        
        db.session.execute("update rodadapontos p set p.ativo=1 where rodada <= (select max(r.id) from rodada r where  r.ativo =1)")
        db.session.execute("update time c set c.pontuacao_total = c.pontuacao_total + (SELECT count(*) FROM account_user WHERE invite = c.user_id)")
        db.session.commit() 
        self.updatePosicaoTimes()
        self.updatePosicaoLigas()
        db.session.commit() 
    
   
        
    def updatePosicaoTimes(self):
        rows = db.session.execute("SELECT id FROM time order by pontuacao_total desc")
        pos=1
        for row in rows:       
            id=row[0]
            db.session.execute("update time set posicao="+str(pos)+"  where id="+str(id))
            pos=pos+1
        db.session.commit()
    
    
  
    def updatePosicaoLigas(self):
        ligas = db.session.execute("SELECT id_liga FROM liga")
        for liga in ligas:
            rows = db.session.execute("SELECT id_ligajogador FROM ligajogador where liga_ligajogador= "+str(liga[0])+" order by pontos_ligajogador desc")
            pos=1
            for row in rows:       
                id=row[0]
                #db.session.execute("update ligajogador set posicaoanterior=posicao  where id_ligajogador="+str(id))
                db.session.execute("update ligajogador set posicao="+str(pos)+"  where id_ligajogador="+str(id))
                
                pos=pos+1
            db.session.commit()
               
    
       
  ###########################
  #UPDATE RODADAS
  
            
    def findRodadaBySemanaAno(self,semana,ano):
        
        db.session.execute("SELECT id FROM rodada where semana=%s and ano=%s",[semana,ano])
        rows = db.session.fetchall()
        for row in rows:
            rodada=row[0]
        print "Rodada id:"+str(rodada)
        return rodada
      

    def updateRodadaInicioFim(self):        
        rows= db.session.execute("SELECT id,adddate( makedate(rodada.ano,rodada.semana*7), interval 2-dayofweek(makedate(rodada.ano,7)) day ) as inicio, adddate( makedate(rodada.ano,rodada.semana*7), interval 8-dayofweek(makedate(rodada.ano,7)) day )  as fim FROM rodada ")
        #rows = db.session.fetchall()
        for row in rows:
            query="update rodada set inicio = '{1}',fim='{2}' where id ={0}".format(row[0],row[1],row[2])
            print query
            db.session.execute(query)
            print "Rodada id:"+str(row[0])
        db.session.commit() 
        self.updateRodadaMaxMinAutomatic()

    
    def removerRodada(self,rodada):               
        #[ ] Delete ponto liga e time
        db.session.execute("delete from rodadapontos where  rodada="+rodada)
        db.session.execute("delete from ligapontos where  rodada_ligapontos="+rodada)
        db.session.commit()         
        
        #[ ] Update rodada ativo 0
        db.session.execute("update  rodada set ativo=0 where id="+rodada)
        db.session.commit()

    def addRodada(self,rodada):
        #delete from rodadapontos where rodada=259 and time>0;
        #insert into rodadapontos SELECT rodada,time,sum(pontos),1 
        #FROM timecandidato tc, pontuacao p where p.candidatura = tc.candidatura 
        #and rodada=259 group by rodada,time;
                
        #delete from ligapontos where rodada_ligapontos=259;
        #insert into   ligapontos SELECT distinct p.rodada,sum(p.pontos),l.liga_ligajogador,l.user_ligajogador  FROM timecandidato tc, pontuacao p,ligajogador l,rodada r WHERE p.candidatura = tc.candidatura and l.user_ligajogador = tc.candidatura and r.id = p.rodada and r.fim >= l.data_ligajogador and rodada=259 group by p.rodada,tc.time,l.liga_ligajogador;
        #update ligajogador l set l.pontos_ligajogador = 
        #(select sum(pontos_ligapontos) from ligapontos where time_ligapontos  = l.user_ligajogador 
        #     and liga_ligapontos     = l.liga_ligajogador group by time_ligapontos,liga_ligapontos) where id_ligajogador>0;
       
        #[ ] Inserir ponto time
        db.session.execute("delete from rodadapontos where rodada="+rodada)
        db.session.execute("insert into rodadapontos SELECT rodada,time,sum(pontos),1 FROM timecandidato tc, pontuacao p where p.candidatura = tc.candidatura and rodada="+rodada+" group by rodada,time")
        db.session.commit()
        
        #[ ] Inserir ponto  liga
        db.session.execute("delete from ligapontos where rodada_ligapontos="+rodada)
        sql="insert into   ligapontos SELECT p.rodada,sum(p.pontos),l.liga_ligajogador,l.user_ligajogador  ";
        sql=sql + "FROM timecandidato tc, pontuacao p,ligajogador l,rodada r ";
        sql=sql + "WHERE p.candidatura = tc.candidatura and l.user_ligajogador = tc.time and ";
        sql=sql + "r.id = p.rodada and r.fim >= l.data_ligajogador and rodada="+rodada+ " group by p.rodada,tc.time,l.liga_ligajogador";
        print sql
        db.session.execute(sql)
        db.session.commit()
        
        sql="update ligajogador l set l.pontos_ligajogador = (select sum(pontos_ligapontos) from ligapontos where time_ligapontos  = l.user_ligajogador "
        sql=sql + " and liga_ligapontos     = l.liga_ligajogador  group by time_ligapontos,liga_ligapontos) "
        db.session.execute(sql)
        db.session.commit()
        self.updateRodadaInicioFim()
        
        #[ ] Set ativo rodada 1
        db.session.execute("update rodada set ativo=1 where id="+rodada)
        db.session.commit()
        
    
    def atualizaRodada(self,rodada,anoatual):
        #[ ] Update ponto partido e candidato total atual (na propria tabela de partido e candidato)
        self.updatePontuacaoCandidatosSQL(anoatual)
        self.updatePontuacaoPartidosSQL()
        #self.updateProposicao()
        #[ ] Update ponto ptime
        self.updatePontuacaoTimesSQL(anoatual)
        
        #tabelas auxiliares de totais durante o tempo (anos.. 2013 , 2014..)
        self.updatePontuacaoCandidatosTotalSQL('2014')
        self.updatePontuacaoPartidosTotalSQL('2014')

        self.updatePontuacaoCandidatosTotalSQL('2013')
        self.updatePontuacaoPartidosTotalSQL('2013')

        #update ponto liga??
        self.updateRodadaInicioFim()
        
        sql="update  despesacandidato d set d.ano =  ( select r.ano from rodada r where d.rodada =  r.id ) where id_despesacandidato >0 and d.ano is null"
        db.session.execute(sql)        
        
        sql="delete FROM ligajogador where user_ligajogador not in (select id from time)"
        db.session.execute(sql)
        
        sql="delete FROM liga where criador_liga not in (select id from time)"
        db.session.execute(sql)
        
        db.session.commit()
        self.cleanRedisCache()
        

    def updateRodadaMaxMinAutomatic(self):
        sqlRodada="SELECT * FROM `rodada` where ativo='1' order by fim desc"
        rows = db.session.execute(sqlRodada)
        
        #MAX
        for row in rows:            
            id=row[0]        
            sql="SELECT max( total_votacao ) , max( total_presenca ) ,  max( total_proposicao ) , max( total_despesa ),min( total_votacao ) , min( total_presenca ) "
            sql=sql+ " ,  min( total_proposicao ) , min( total_despesa ),avg( total_votacao ) , avg( total_presenca ) ,  avg( total_proposicao ) , avg( total_despesa )"
            sql=sql+" , max( pontos ),min( pontos ),avg( pontos ),rodada FROM `pontuacao` where rodada = "+str(id)+" group by rodada"
            print sql
            novos = db.session.execute(sql)
            #novos = db.session.fetchall()
            for novo in novos:  
                print novo[0]              
                sql="update rodada set max_votacao="+ str(novo[0])+ ", max_presenca="+ str(novo[1])+ ",max_proposicao="+ str(novo[2])+ ",max_despesa="+ str(novo[3])
                sql=sql+ ",min_votacao="+ str(novo[4])+ ", min_presenca="+ str(novo[5])+ ",min_proposicao="+ str(novo[6])+ ",min_despesa="+ str(novo[7])
                sql=sql+ ", avg_votacao="+ str(novo[8])+ ", avg_presenca="+ str(novo[9])+ ",avg_proposicao="+ str(novo[10])+ ",avg_despesa="+ str(novo[11])
                sql=sql+ ", max_pontuacao="+ str(novo[12])+ ", min_pontuacao="+ str(novo[13])+ ",avg_pontuacao="+ str(novo[14])
                sql=sql+ "  where id="+ str(novo[15])
                print sql
                db.session.execute(sql)
                #db.session.execute("update rodada set max_votacao=%s, max_presenca=%s,max_proposicao=%s,max_despesa=%s where id=%s",[novo[0],novo[1],novo[2],novo[3],novo[4]])
        db.session.commit()
        
        
###########
# GERAL
###########

    def getIPUser(self,request):
        if not request.headers.getlist("X-Forwarded-For"):
           ip = request.remote_addr
        else:
           ip = request.headers.getlist("X-Forwarded-For")[0]
        return ip        
    
    def cleanRedisCache(self):
        import redis
        r = redis.Redis()
        for cache_key in r.keys():
            if "session:" not in cache_key:
                r.delete(cache_key)
            else:
                print cache_key
    def votacaoSimilarCandidato(self):
        sql="SELECT vc.candidatura as candidatura1,vc2.candidatura  as candidatura2,count(*) "
        sql=sql+"FROM votacaocandidato vc, votacaocandidato vc2 where vc.candidatura <> vc2.candidatura "
        sql=sql+"and vc.voto = vc2.voto and vc.proposicao = vc2.proposicao group by vc.candidatura,vc2.candidatura "
        return db.session.execute(sql)
        
