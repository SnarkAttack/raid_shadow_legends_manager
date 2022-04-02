from logging import _levelToName
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from rsl_manager.db_objs.utilities import cm_session_managed, s_session_managed
from ._db_core import Base, engine
from sqlalchemy.sql import null, not_
from rsl_manager.enums import ArtifactTypes, ArtifactSets

class ArtifactBonus(Base):
    id = Column(Integer, primary_key=True)
    glyph_power = Column(Float)
    level = Column(Integer)
    kind = Column(Integer)
    absolute = Column(Boolean)
    value = Column(Float)
    artifact_id = Column(Integer, ForeignKey('artifact.id'))

class PrimaryArtifactBonus(ArtifactBonus):
    artifact = relationship("Artifact", back_populates="primary_bonus", uselist=False, lazy='dynamic')

class SecondaryArtifactBonus(ArtifactBonus):
    artifact = relationship("Artifact", back_populates="secondary_bonuses", lazy='dynamic')

class Artifact(Base):

    id = Column(Integer, primary_key=True)
    type = Column(Integer)
    set_type = Column(Integer)
    rank = Column(Integer)
    rarity = Column(Integer)
    level = Column(Integer)
    faction = Column(Integer)
    seen = Column(Boolean)
    activated = Column(Boolean)
    sell_price = Column(Integer)
    price = Column(Integer)
    failed_upgrades = Column(Integer)
    # Primary bonus
    primary_bonus = relationship("PrimaryArtifactBonus", back_populates="artifact", lazy='dynamic')
    secondary_bonuses = relationship("SeconaryArtifactBonus", back_populates="artifact", lazy='dynamic')
    revision = Column(Integer)

    @classmethod
    @cm_session_managed(engine)
    def artifact_from_json(cls, session, artifact_json):

        artifact_id = artifact_json['id']

        existing_artifact = session.query(cls).filter_by(id=artifact_id).first()

        # If artifact already exists, get previously created bonuses so we can update them
        if existing_artifact:
            primary_bonus = existing_artifact.primary_bonus
            secondary_bonuses = existing_artifact.seconary_bonuses

        else:

            artifact = Artifact(
                            id=artifact_json['id'],
                            kind=
            )

            session.merge(owned_champ)