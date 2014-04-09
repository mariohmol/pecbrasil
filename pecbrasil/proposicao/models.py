from pecbrasil import db
from pecbrasil.utils import AutoSerialize
from pecbrasil.politica.models import Candidatura,Time
from pecbrasil.account.models import User


class TipoProposicao(db.Model, AutoSerialize):
    __tablename__ = 'tipoproposicao'
    __public__ = ('id_tipoproposicao',   'nome_tipoproposicao','sigla_tipoproposicao','originalid_tipoproposicao')
    id_tipoproposicao = db.Column(db.Integer, primary_key=True)
    nome_tipoproposicao = db.Column(db.Text())
    sigla_tipoproposicao = db.Column(db.Text())   
    originalid_tipoproposicao = db.Column(db.Integer)
    proposicoes = db.relationship("Proposicao", backref = 'tipoproposicao', lazy = 'dynamic')
    def __repr__(self):
        return '<TipoProposicao %r>' % (self.time)
    
class StatusProposicao(db.Model, AutoSerialize):
    __tablename__ = 'statusproposicao'
    __public__ = ('id_statusproposicao', 'nome_statusproposicao',  'originalid_statusproposicao', 'sigla_statusproposicao')
    id_statusproposicao = db.Column(db.Integer, primary_key=True)
    nome_statusproposicao = db.Column(db.Text())
    sigla_statusproposicao=db.Column(db.Text())
    originalid_statusproposicao=db.Column(db.Integer)
    proposicoes = db.relationship("Proposicao", backref = 'statusproposicao', lazy = 'dynamic')
    def __repr__(self):
        return '<StatusProposicao %r>' % (self.time)

class Proposicao(db.Model, AutoSerialize):
    __tablename__ = 'proposicao'
    __public__ = ('status', 'id',  'desc','sigla')
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(30), primary_key=True)
    status = db.Column(db.String(30),db.ForeignKey(StatusProposicao.id_statusproposicao))
    desc = db.Column(db.Text())
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id))
    data = db.Column(db.Date)
    datavotacao = db.Column(db.Date)
    tipo = db.Column(db.Integer,db.ForeignKey(TipoProposicao.id_tipoproposicao))
    favor = db.Column(db.Integer)
    contra = db.Column(db.Integer)
    abstencao = db.Column(db.Integer)
    votacaocandidato = db.relationship("VotacaoCandidato", backref = 'proposicoes', lazy = 'dynamic')
    timevotacao = db.relationship("TimeVotacao", backref = 'proposicoes', lazy = 'dynamic')
    def __repr__(self):
        return '<Proposicao %r>' % (self.id)

    
class ProposicaoAcao(db.Model, AutoSerialize):
    __tablename__ = 'proposicaoacao'
    __public__ = ('id_proposicaoacao', 'nome_proposicaoacao',  'originalid_proposicaoacao', 'proposicao_proposicaoacao','data_proposicaoacao','status_proposicaoacao')
    id_proposicaoacao = db.Column(db.Integer, primary_key=True)
    nome_proposicaoacao = db.Column(db.Text())
    originalid_proposicaoacao=db.Column(db.Integer)
    data_proposicaoacao=db.Column(db.Date)
    proposicao_proposicaoacao=db.Column(db.Integer,db.ForeignKey(Proposicao.id))    
    status_proposicaoacao=db.Column(db.Integer,db.ForeignKey(StatusProposicao.id_statusproposicao))
    def __repr__(self):
        return '<ProposicaoAcao %r>' % (self.time)
    
      
         
class VotacaoCandidato(db.Model, AutoSerialize):
    __tablename__ = 'votacaocandidato'
    __public__ = ('proposicao', 'candidatura',  'voto')
    proposicao = db.Column(db.Integer, db.ForeignKey(Proposicao.id), primary_key=True)
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id), primary_key=True)
    voto = db.Column(db.Integer)
    def __repr__(self):
        return '<VotacaoCandidato %r>' % (self.voto)


class TimeVotacao(db.Model, AutoSerialize):
    __tablename__ = 'timevotacao'
    __public__ = ('time', 'votacao',  'voto','data','necessidade','desc')
    time = db.Column(db.Integer, db.ForeignKey(Time.id), primary_key=True)
    proposicao = db.Column(db.Integer,db.ForeignKey(Proposicao.id), primary_key=True)
    voto = db.Column(db.Integer)
    necessidade = db.Column(db.Integer)
    data = db.Column(db.Date)
    desc = db.Column(db.Text())
    def __repr__(self):
        return '<TimeVotacao %r>' % (self.time)
 
class Repasse(db.Model, AutoSerialize):
    __tablename__ = 'repasse'
    __public__ = ('proposicao',   'valor','desc')
    desc = db.Column(db.Text())
    proposicao = db.Column(db.Integer,db.ForeignKey(Proposicao.id), primary_key=True)
    valor = db.Column(db.Integer)
    def __repr__(self):
        return '<Repasse %r>' % (self.proposicao)
    