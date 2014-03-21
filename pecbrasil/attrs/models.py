from pecbrasil import db, __latest_year__
from pecbrasil.utils import AutoSerialize, exist_or_404
from sqlalchemy import func, Float
from sqlalchemy.sql.expression import cast

from flask import g



############################################################
# ----------------------------------------------------------
# Geography
# 
############################################################ 


class Wld(db.Model, AutoSerialize):

    __tablename__ = 'attrs_wld'
    __public__ = ('id', 'id_3char', 'name_en', 'name_pt', 'color')
    id = db.Column(db.String(5), primary_key=True)
    id_2char = db.Column(db.String(2))
    id_3char = db.Column(db.String(3))
    id_num = db.Column(db.Integer())
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    gender_pt = db.Column(db.SmallInteger)
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
  
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/wld/wld_%s.png" % (self.id)
        
    def __repr__(self):
        return '<Wld %r>' % (self.id_3char)

bra_pr = db.Table('attrs_bra_pr',
    db.Column('bra_id', db.Integer, db.ForeignKey('attrs_bra.id')),
    db.Column('pr_id', db.Integer, db.ForeignKey('attrs_bra.id'))
)

class Bra(db.Model, AutoSerialize):

    __tablename__ = 'attrs_bra'
    __public__ = ('id', 'id_ibge', 'name_en', 'name_pt', 'color', 'distance')
    id = db.Column(db.String(10), primary_key=True)
    id_ibge = db.Column(db.Integer())
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())
    
    distance = 0
    
   
    # Neighbors
    neighbors = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_origin)", backref='bra_origin', lazy='dynamic')
    bb = db.relationship('Distances', primaryjoin = "(Bra.id == Distances.bra_id_dest)", backref='bra', lazy='dynamic')
   
    def name(self):
        lang = getattr(g, "locale", "en")
        return getattr(self,"name_"+lang)
        
    def icon(self):
        return "/static/img/icons/bra/bra_%s.png" % (self.id[:2])

    def get_neighbors(self, dist, remove_self=False):
        q = self.neighbors.filter(Distances.distance <= dist).order_by(Distances.distance)
        if remove_self:
            q = q.filter(Distances.bra_id_dest != self.id) # filter out self
        return q.all()

    def __repr__(self):
        return '<Bra %r>' % (self.name_en)

############################################################
# ----------------------------------------------------------
# Attr data
# 
############################################################

class Distances(db.Model):

    __tablename__ = 'attrs_bb'
    bra_id_origin = db.Column(db.String(10), db.ForeignKey('attrs_bra.id'), primary_key=True)
    bra_id_dest = db.Column(db.String(10), db.ForeignKey('attrs_bra.id'), primary_key=True)
    distance = db.Column(db.Float())

    def __repr__(self):
        return '<Bra_Dist %r-%r:%g>' % (self.bra_id_origin, self.bra_id_dest, self.distance)

    def serialize(self):
        return {
            "bra_id_origin": self.bra_id_origin,
            "bra_id_dest": self.bra_id_dest,
            "distance": self.distance
        }
