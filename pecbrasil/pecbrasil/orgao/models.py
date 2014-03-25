from pecbrasil import db
from pecbrasil.utils import AutoSerialize
from pecbrasil.politica.models import Candidatura,Time
from pecbrasil.account.models import User

class Orgao(db.Model, AutoSerialize):
    __tablename__ = 'orgao'
    __public__ = ('status', 'id',  'desc','sigla','original_cf','totalmembros')
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(30), primary_key=True)
    tipo = db.Column(db.Integer)
    totalmembros = db.Column(db.Integer)
    desc = db.Column(db.Text())
    orgaocandidato = db.relationship("OrgaoCandidato", backref = 'orgaos', lazy = 'dynamic')
    def __repr__(self):
        return '<Orgao %r>' % (self.id)
    
class OrgaoCandidato(db.Model, AutoSerialize):
    __tablename__ = 'orgaocandidato'
    __public__ = ('orgao', 'candidatura',  'cargo','id')
    id = db.Column(db.Integer, primary_key=True)
    orgao = db.Column(db.Integer, db.ForeignKey(Orgao.id), primary_key=True)
    candidatura = db.Column(db.Integer,db.ForeignKey(Candidatura.id), primary_key=True)
    cargo = db.Column(db.Integer)
    def __repr__(self):
        return '<OrgaoCandidato %r>' % (self.voto)

class TipoOrgao(db.Model, AutoSerialize):
    __tablename__ = 'tipoorgao'
    __public__ = ('id',   'nome','desc','original_cf')
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text())
    desc = db.Column(db.Text())   
    original_cf = db.Column(db.Integer)
    def __repr__(self):
        return '<TipoOrgao %r>' % (self.time)
    