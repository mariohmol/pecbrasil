from pecbrasil import db
from pecbrasil.utils import AutoSerialize
from pecbrasil.account.models import User
from pecbrasil.politica.models import Rodada,Time

class Liga(db.Model, AutoSerialize):

    __tablename__ = 'liga'
    __public__ = ('id_liga', 'nome_liga', 'criador_liga', 'data_liga')
    id_liga = db.Column(db.Integer, primary_key=True)
    nome_liga = db.Column(db.String(150))
    criador_liga = db.Column(db.Integer, db.ForeignKey(Time.id))
    data_liga = db.Column(db.DateTime)
    publico_liga = db.Column(db.Integer)
    desc_liga = db.Column(db.Text)   
    ligajogador = db.relationship("LigaJogador", backref = 'liga', lazy = 'dynamic')
    
    def __repr__(self):
        return '<Liga %r>' % (self.nome_liga)


class LigaJogador(db.Model, AutoSerialize):

    __tablename__ = 'ligajogador'
    __public__ = ('id_ligajogador', 'user_ligajogador', 'data_ligajogador', 'liga_ligajogador','status_ligajogador')
    id_ligajogador = db.Column(db.Integer, primary_key=True)
    user_ligajogador = db.Column(db.Integer, db.ForeignKey(Time.id))
    data_ligajogador = db.Column(db.DateTime)
    liga_ligajogador = db.Column(db.Integer, db.ForeignKey(Liga.id_liga))
    status_ligajogador = db.Column(db.Integer, default=1)  
    pontos_ligajogador = db.Column(db.Integer)
    posicao = db.Column(db.Integer)
    def __repr__(self):
        return '<LigaJogador %r>' % (self.id_ligajogador)
    
class LigaPontos(db.Model, AutoSerialize):

    __tablename__ = 'ligapontos'
    __public__ = ('liga_ligapontos','time_ligapontos',  'rodada_ligapontos', 'pontos_ligapontos')
    liga_ligapontos = db.Column(db.Integer, db.ForeignKey(Liga.id_liga), primary_key=True)
    time_ligapontos = db.Column(db.Integer, db.ForeignKey(Time.id), primary_key=True)
    rodada_ligapontos = db.Column(db.Integer, db.ForeignKey(Rodada.id), primary_key=True)
    pontos_ligapontos = db.Column(db.Integer)
    
    def __repr__(self):
        return '<LigaPontos %r>' % (self.ligajogador_ligapontos)
    

class Convite(db.Model, AutoSerialize):

    __tablename__ = 'convite'
    __public__ = ('id_convite','usuario',  'email', 'dataenvio')
    id_convite = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    email = db.Column(db.String(150))
    dataenvio = db.Column(db.DateTime)
    datacadastro = db.Column(db.DateTime)
    dataponto = db.Column(db.DateTime)
    
    
    
