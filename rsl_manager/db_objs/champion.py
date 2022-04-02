from logging import _levelToName
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from rsl_manager.enums import Locations
from rsl_manager.db_objs.utilities import cm_session_managed, s_session_managed
from ._db_core import Base, engine
from sqlalchemy.sql import null, not_
from rsl_manager.db_objs import Rating


class Champion(Base):
    __tablename__ = 'champions'

    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    affinity = Column(Integer)
    faction = Column(Integer)
    role = Column(Integer)
    rarity = Column(Integer)
    owned = relationship("OwnedChampion", back_populates="champion", lazy='dynamic')
    ratings = relationship("Rating", back_populates="champion", lazy='dynamic')
    
    @classmethod
    def get_champion_from_name(cls, session, name):
        champion = session.query(cls).filter_by(name=name).first()
        return champion

    @classmethod
    def get_all_champions(cls, session):
        return session.query(cls).all()

    @classmethod
    @cm_session_managed(engine)
    def get_champ_id_from_name(cls, session, name):
        champion = session.query(cls).filter_by(name=name).first()
        if champion is not None:
            return champion.id
        return None

    @classmethod
    @cm_session_managed
    def get_all_names(cls, session):
        champ_names = [champ.name for champ in  session.query(cls).all()]
        return list(set(champ_names))

    @classmethod
    def get_champions_by_faction(cls, session, faction):
        return session.query(cls).filter_by(faction=faction).all()

    @classmethod
    def get_champions_by_rarity(cls, session, rarity):
        return session.query(cls).filter_by(rarity=rarity).all()

    def get_overall_rating(self):
        valid_ratings = self.ratings.filter(Rating.overall_rating != null()).all()
        overall_rating = round(sum([rating.overall_rating for rating in valid_ratings])/len(valid_ratings), 2)
        return overall_rating

    def get_location_rating(self, location):
        location_name = location.name
        rating_name = f"{location_name.lower()}_rating"
        location_ratings = self.ratings.filter(getattr(Rating, rating_name) != null()).all()
        if len(location_ratings) == 0:
            return 'NA'
        avg_location_rating = round(sum([getattr(rating, rating_name) for rating in location_ratings])/len(location_ratings), 2)
        return avg_location_rating


class OwnedChampion(Base):
    __tablename__ = 'owned_champions'

    id = Column(Integer, primary_key=True)
    level = Column(Integer)
    empower_level = Column(Integer)
    exp = Column(Integer)
    full_exp = Column(Integer)
    deleted = Column(Boolean)
    locked = Column(Boolean)
    in_vault = Column(Boolean)
    champion_id = Column(Integer, ForeignKey('champions.id'))
    champion = relationship("Champion", back_populates="owned")

    @classmethod
    def get_all_owned_champions(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_all_unique_owned_champions(cls, session):
        unique_ids = cls.get_all_unique_champion_ids()
        return [session.query(Champion).filter(Champion.id==id).first() for id in unique_ids]

    @classmethod
    @cm_session_managed(engine)
    def champ_from_json(cls, session, champ_json):

        owned_champ = OwnedChampion(
                        id=champ_json['id'],
                        level=champ_json['level'],
                        empower_level=champ_json['empowerLevel'],
                        exp=champ_json['exp'],
                        full_exp=champ_json['fullExp'],
                        deleted=champ_json['deleted'],
                        locked=champ_json['locked'],
                        in_vault=champ_json['inVault'],
                        champion_id=Champion.get_champ_id_from_name(champ_json['name'])
        )

        session.merge(owned_champ)

    @classmethod
    @cm_session_managed(engine)
    def get_all_unique_names(cls, session):
        owned_champion_names = [owned_champ.champion.name for owned_champ in session.query(cls).all()]
        return list(set(owned_champion_names))

    @classmethod
    @cm_session_managed(engine)
    def get_all_unique_champion_ids(cls, session):
        owned_champion_ids = [owned_champion.champion_id for owned_champion in session.query(cls).all()]
        return list(set(owned_champion_ids))

    @classmethod
    def get_owned_champions_by_faction(cls, session, faction):
        return session.query(cls).filter(OwnedChampion.champion.has(faction=faction)).all()

    @classmethod
    def get_champions_by_faction(cls, session, faction):
        return [c.champion for c in cls.get_owned_champions_by_faction(session, faction)]

    @classmethod
    def get_owned_champions_by_rarity(cls, session, rarity):
        return session.query(cls).filter(OwnedChampion.champion.has(rarity=rarity)).all()

    @classmethod
    def get_champions_by_rarity(cls, session, rarity):
        return [c.champion for c in cls.get_owned_champions_by_rarity(session, rarity)]