from pecbrasil import db
from pecbrasil.utils import AutoSerialize
from pecbrasil.account.models import User

#EXEMPLOS:
# isic_id = db.Column(db.String(5), db1.ForeignKey(Isic.id), primary_key=True)
# partido = db.relationship("Partido", backref = 'politico', lazy = 'dynamic')


class Partido(db.Model, AutoSerialize):

    __tablename__ = 'partido'
    __public__ = ('id', 'name_en', 'name_pt', 'color','sigla', 'politico_total',  \
                    'pontuacao_total',    'pontuacao_ultima',    'pontuacao_tendencia', 'pontuacao_total_media', \
                       'total_votacao',    'total_presenca' ,    'total_processo' ,   'total_proposicao' ,    'total_despesa' )
    id = db.Column(db.String(5), primary_key=True)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    sigla = db.Column(db.String(20))
    codigo = db.Column(db.String(50))  
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
    color = db.Column(db.String(7))
    politico_total = db.Column(db.Integer)
    pontuacao_total_media = db.Column(db.Integer)
    pontuacao_total = db.Column(db.Integer)
    pontuacao_ultima = db.Column(db.Integer)
    pontuacao_tendencia = db.Column(db.Integer)    
    total_votacao = db.Column(db.Integer)
    total_presenca = db.Column(db.Integer)
    total_processo = db.Column(db.Integer)
    total_proposicao = db.Column(db.Integer)  
    total_despesa = db.Column(db.Integer)  
    politico = db.relationship("Politico", backref = 'partidos', lazy = 'dynamic')
    candidaturas = db.relationship("Candidatura", backref = 'partidos', lazy = 'dynamic')
    partidototal = db.relationship("PartidoTotal", backref = 'partidos', lazy = 'dynamic')
    
    def __repr__(self):
        return '<Partido %r>' % (self.name_en)


class Politico(db.Model, AutoSerialize):

    __tablename__ = 'politico'
    __public__ = ('id', 'nome', 'nascimento', 'id_original')
    id = db.Column(db.Integer, primary_key=True)
    id_original = db.Column(db.Integer)
    nome = db.Column(db.String(200))
    nascimento = db.Column(db.DateTime)
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())  
    partido = db.Column(db.String(5), db.ForeignKey(Partido.id))  
    candidaturas = db.relationship("Candidatura", backref = 'politicos', lazy = 'dynamic')
        
    def __repr__(self):
        return '<Politico %r>' % (self.nome)



class Candidatura(db.Model, AutoSerialize):

    __tablename__ = 'candidatura'
    __public__ = ('id','id_original','name_pt', 'name_en', 'politico', 'color' , 'partido', 'uf',\
                   'cidade','pontuacao_total','pontuacao_ultima','pontuacao_tendencia'\
                   ,'total_votacao','total_presenca','total_processo','total_proposicao','total_despesa')
    id = db.Column(db.Integer, primary_key=True)
    id_original = db.Column(db.Integer)
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
    uf = db.Column(db.String(50))
    cidade = db.Column(db.String(200))
    cargo = db.Column(db.String(200))
    situacao = db.Column(db.String(200))    
    email = db.Column(db.String(200))  
    inicio = db.Column(db.DateTime)
    fim = db.Column(db.DateTime)
    color = db.Column(db.String(7))
    pontuacao_total = db.Column(db.Integer)
    pontuacao_ultima = db.Column(db.Integer)
    pontuacao_tendencia = db.Column(db.Integer)    
    total_votacao = db.Column(db.Integer)
    total_presenca = db.Column(db.Integer)
    total_processo = db.Column(db.Integer)
    total_proposicao = db.Column(db.Integer)  
    total_despesa = db.Column(db.Integer)    
    partido = db.Column(db.Integer, db.ForeignKey(Partido.id))
    politico = db.Column(db.Integer, db.ForeignKey(Politico.id))     
    times = db.relationship("TimeCandidato", backref = 'candidatos', lazy = 'dynamic')
    despesas = db.relationship("DespesaCandidato", backref = 'candidaturas', lazy = 'dynamic')
    proposicoes = db.relationship("Proposicao", backref = 'candidaturas', lazy = 'dynamic')
    orgaos = db.relationship("OrgaoCandidato", backref = 'candidaturas', lazy = 'dynamic')
    votacoescandidato = db.relationship("VotacaoCandidato", backref = 'candidaturas', lazy = 'dynamic')
    pontuacoes = db.relationship("Pontuacao", backref = 'candidaturas', lazy = 'dynamic')
    candidaturatotal = db.relationship("CandidaturaTotal", backref = 'candidaturas', lazy = 'dynamic')
    def __repr__(self):
        return '<Candidatura %r>' % (self.name_en)


class Rodada(db.Model, AutoSerialize):

    __tablename__ = 'rodada'
    __public__ = ('id','nome_rodada', 'inicio', 'fim','ano','semana','ativo','max_presenca','min_presenca','avg_presenca','max_proposicao','min_proposicao','avg_proposicao', \
                  'max_processo','min_processo','max_votacao','min_votacao','avg_votacao','max_despesa','min_despesa','avg_despesa')
    id = db.Column(db.Integer, primary_key=True)
    inicio = db.Column(db.DateTime)
    fim = db.Column(db.DateTime)
    semana = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    ativo  = db.Column(db.Integer)
    despesa = db.relationship("DespesaCandidato", backref = 'rodadas', lazy = 'dynamic')
    pontuacoes = db.relationship("Pontuacao", backref = 'rodadas', lazy = 'dynamic')
    nome_rodada = db.Column(db.String(50))
    
    max_pontuacao  = db.Column(db.Integer)
    min_pontuacao  = db.Column(db.Integer)  
    avg_pontuacao  = db.Column(db.Integer)  
    max_presenca  = db.Column(db.Integer)
    min_presenca  = db.Column(db.Integer)
    avg_presenca  = db.Column(db.Integer)
    max_proposicao  = db.Column(db.Integer)
    min_proposicao  = db.Column(db.Integer)
    avg_proposicao  = db.Column(db.Integer)
    max_processo  = db.Column(db.Integer)
    min_processo  = db.Column(db.Integer)
    max_votacao   = db.Column(db.Integer)
    min_votacao  = db.Column(db.Integer)
    avg_votacao  = db.Column(db.Integer)
    max_despesa  = db.Column(db.Integer)
    min_despesa  = db.Column(db.Integer)
    avg_despesa  = db.Column(db.Integer)
    def __repr__(self):
        return '<Rodada %r>' % (self.inicio)

    


class Pontuacao(db.Model, AutoSerialize):

    __tablename__ = 'pontuacao'
    __public__ = ('rodada', 'candidatura', 'pontos',                  
                  'presenca' ,'tendencia_presenca' ,  'total_presenca' ,
                        'proposicao' ,  'tendencia_proposicao' ,   'total_proposicao' ,
                        'processo' ,   'tendencia_processo', 'total_processo' ,  
                    'votacao' ,    'tendencia_votacao' , 'total_votacao' , 
                    'despesa' , 'tendencia_despesa',  'total_despesa',
                    'rodada_ano','rodada_numero','atualizado'
                     )
    rodada = db.Column(db.Integer, db.ForeignKey(Rodada.id), primary_key=True)
    rodada_ano = db.Column(db.Integer)
    rodada_numero = db.Column(db.Integer)
    candidatura = db.Column(db.Integer, db.ForeignKey(Candidatura.id), primary_key=True)
    ativo = db.Column(db.Integer)
    pontos = db.Column(db.Integer)
    presenca = db.Column(db.Integer)
    tendencia_presenca = db.Column(db.Integer)
    total_presenca = db.Column(db.Integer)
    proposicao = db.Column(db.Integer)
    tendencia_proposicao = db.Column(db.Integer)
    total_proposicao = db.Column(db.Integer)
    processo = db.Column(db.Integer)
    tendencia_processo = db.Column(db.Integer)
    total_processo = db.Column(db.Integer)
    votacao = db.Column(db.Integer)
    tendencia_votacao = db.Column(db.Integer)
    total_votacao = db.Column(db.Integer)
    despesa = db.Column(db.Integer)
    tendencia_despesa = db.Column(db.Integer)
    total_despesa = db.Column(db.Integer)
    atualizado = db.Column(db.Date)
    def __repr__(self):
        return '<Pontuacao %r>' % (self.rodada)



class Time(db.Model, AutoSerialize):
    __tablename__ = 'time'
    __public__ = ('id', 'nome',  'color','fundacao','pontuacao_total','posicao')
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    fundacao = db.Column(db.DateTime)
    desc = db.Column(db.Text())
    keywords = db.Column(db.String(100))
    color = db.Column(db.String(7))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    pontuacao_total = db.Column(db.Integer)
    pontuacao_ultima = db.Column(db.Integer)
    pontuacao_tendencia = db.Column(db.Integer)
    posicao = db.Column(db.Integer)
    candidatos = db.relationship("TimeCandidato", backref = 'times', lazy = 'dynamic')
    votacoes = db.relationship("TimeVotacao", backref = 'times', lazy = 'dynamic')
    rodadapontos = db.relationship("RodadaPontos", backref = 'times', lazy = 'dynamic')
    ligajogador = db.relationship("LigaJogador", backref = 'time', lazy = 'dynamic') 
    liga = db.relationship("Liga", backref = 'criador_time', lazy = 'dynamic') 
       
    def __repr__(self):
        return '<Time %r>' % (self.nome)


class TimeCandidato(db.Model, AutoSerialize):
    __tablename__ = 'timecandidato'
    __public__ = ('time', 'candidatura',  'posicao')
    time = db.Column(db.Integer, db.ForeignKey(Time.id), primary_key=True)
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id), primary_key=True)
    posicao = db.Column(db.Integer)
    def __repr__(self):
        return '<TimeCandidato %r>' % (self.time)

   
class RodadaPontos(db.Model, AutoSerialize):

    __tablename__ = 'rodadapontos'
    __public__ = ('pontos', 'rodada', 'time')
    rodada = db.Column(db.Integer, db.ForeignKey(Rodada.id), primary_key=True)
    time = db.Column(db.Integer, db.ForeignKey(Time.id), primary_key=True)
    ativo = db.Column(db.Integer)
    pontos = db.Column(db.Integer)

    def __repr__(self):
        return '<RodadaPontos %r>' % (self.rodada)
    
class ProcessoCandidato(db.Model, AutoSerialize):
    __tablename__ = 'processocandidato'
    __public__ = ('processo', 'candidatura',  'status',  'desc','categoria')
    processo = db.Column(db.String(50), primary_key=True)
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id), primary_key=True)
    status = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    desc = db.Column(db.Text())
    def __repr__(self):
        return '<ProcessoCandidato %r>' % (self.time)


class DespesaTipo(db.Model, AutoSerialize):
    __tablename__ = 'despesatipo'
    __public__ = ('nome_despesatipo',   'cor_despesatipo','id_despesatipo','desc_despesatipo')
    nome_despesatipo = db.Column(db.String(150))
    cor_despesatipo = db.Column(db.String(10))
    desc_despesatipo = db.Column(db.Text())
    id_despesatipo = db.Column(db.Integer,primary_key=True)
    despesas = db.relationship("DespesaCandidato", backref = 'categorias', lazy = 'dynamic')
    
    def __repr__(self):
        return '<DespesaTipo %r>' % (self.time)  
    
class DespesaCandidato(db.Model, AutoSerialize):
    __tablename__ = 'despesacandidato'
    __public__ = ('categoria', 'candidatura',  'valor','rodada','idcategoria','ano')
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id), primary_key=True)
    valor = db.Column(db.Integer)
    rodada = db.Column(db.Integer,db.ForeignKey(Rodada.id), primary_key=True)
    ativo = db.Column(db.Integer)
    ano = db.Column(db.Integer)
    categoria = db.Column(db.Integer,db.ForeignKey(DespesaTipo.id_despesatipo), primary_key=True)
    idcategoria= db.Column(db.String(60), primary_key=True)
    def __repr__(self):
        return '<DespesaCandidato %r>' % (self.time)
    

#Tabela que tem os dados ja pre calculados
class PartidoTotal(db.Model, AutoSerialize):

    __tablename__ = 'partidototal'
    __public__ = ('id','sigla','ano', 'politico_total','partidos',  \
                    'pontuacao_total',    'pontuacao_ultima',    'pontuacao_tendencia', 'pontuacao_total_media', \
                       'total_votacao',    'total_presenca' ,    'total_processo' ,   'total_proposicao' ,    'total_despesa' )
    id = db.Column(db.String(5), primary_key=True)
    sigla = db.Column(db.String(20))
    codigo = db.Column(db.String(50))  
    politico_total = db.Column(db.Integer)
    pontuacao_total_media = db.Column(db.Integer)
    pontuacao_total = db.Column(db.Integer)
    pontuacao_ultima = db.Column(db.Integer)
    pontuacao_tendencia = db.Column(db.Integer)    
    total_votacao = db.Column(db.Integer)
    total_presenca = db.Column(db.Integer)
    total_processo = db.Column(db.Integer)
    total_proposicao = db.Column(db.Integer)  
    total_despesa = db.Column(db.Integer)  
    ano = db.Column(db.Integer)  
    partido = db.Column(db.Integer, db.ForeignKey(Partido.id))
    def __repr__(self):
        return '<PartidoTotal %r>' % (self.name_en)



class CandidaturaTotal(db.Model, AutoSerialize):

    __tablename__ = 'candidaturatotal'
    __public__ = ('id','candidatura','ano','votacao_total','presenca_total','processo_total','proposicao_total')
    id = db.Column(db.Integer, primary_key=True)
    pontuacao_total = db.Column(db.Integer)
    pontuacao_ultima = db.Column(db.Integer)
    pontuacao_tendencia = db.Column(db.Integer)    
    total_votacao = db.Column(db.Integer)
    total_presenca = db.Column(db.Integer)
    total_processo = db.Column(db.Integer)
    total_proposicao = db.Column(db.Integer)  
    total_despesa = db.Column(db.Integer) 
    ano = db.Column(db.Integer)     
    partido = db.Column(db.Integer, db.ForeignKey(Partido.id))
    candidatura = db.Column(db.Integer, db.ForeignKey(Candidatura.id))     
   
    def __repr__(self):
        return '<CandidaturaTotal %r>' % (self.name_en)

