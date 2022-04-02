from logging import _levelToName
from operator import not_
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.sql import null, not_
from sqlalchemy.orm import relationship
from rsl_manager.enums import Locations
from rsl_manager.db_objs.utilities import cm_session_managed
from rsl_manager.enums.named_int_enum import DataSources
from ._db_core import Base, engine

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    champion_id = Column(Integer, ForeignKey("champions.id"))
    source = Column(Integer)
    overall_rating = Column(Float)
    campaign_rating = Column(Float)
    arena_atk_rating = Column(Float)
    arena_def_rating = Column(Float)
    clan_boss_rating = Column(Float)
    faction_wars_rating = Column(Float)
    doom_tower_waves_rating = Column(Float)
    spider_rating = Column(Float)
    fire_knight_rating = Column(Float)
    dragon_rating = Column(Float)
    ice_golem_rating = Column(Float)
    minotaur_rating = Column(Float)
    arcane_keep_rating = Column(Float)
    force_keep_rating = Column(Float)
    spirit_keep_rating = Column(Float)
    magic_keep_rating = Column(Float)
    void_keep_rating = Column(Float)
    magma_dragon_rating = Column(Float)
    frost_spider_rating = Column(Float)
    nether_spider_rating = Column(Float)
    scarab_king_rating = Column(Float)
    eternal_dragon_rating = Column(Float)
    celestial_griffin_rating = Column(Float)
    dreadhorn_rating = Column(Float)
    dark_fae_rating = Column(Float)

    champion = relationship("Champion", back_populates="ratings")

    @classmethod
    @cm_session_managed(engine)
    def from_rating_parser(cls, session, champ_name, rating_results, parser_name):
        from rsl_manager.db_objs import Champion
        champion_id = Champion.get_champ_id_from_name(champ_name)
        data_source = DataSources.from_code(parser_name)
        overall_rating = rating_results[0]
        coded_location_ratings = {Locations.from_code(area_name): rating for area_name, rating in rating_results[1]}
        rating = Rating(
                    champion_id = champion_id,
                    source = data_source,
                    overall_rating = overall_rating,
                    campaign_rating = coded_location_ratings.get(Locations.CAMPAIGN, null()),
                    arena_atk_rating = coded_location_ratings.get(Locations.ARENA_ATK, null()),
                    arena_def_rating = coded_location_ratings.get(Locations.ARENA_DEF, null()),
                    clan_boss_rating = coded_location_ratings.get(Locations.CLAN_BOSS, null()),
                    faction_wars_rating = coded_location_ratings.get(Locations.FACTION_WARS, null()),
                    doom_tower_waves_rating = coded_location_ratings.get(Locations.DOOM_TOWER_WAVES, null()),
                    spider_rating = coded_location_ratings.get(Locations.SPIDER, null()),
                    fire_knight_rating = coded_location_ratings.get(Locations.FIRE_KNIGHT, null()),
                    dragon_rating = coded_location_ratings.get(Locations.DRAGON, null()),
                    ice_golem_rating = coded_location_ratings.get(Locations.ICE_GOLEM, null()),
                    minotaur_rating = coded_location_ratings.get(Locations.MINOTAUR, null()),
                    arcane_keep_rating = coded_location_ratings.get(Locations.ARCANE_KEEP, null()),
                    force_keep_rating = coded_location_ratings.get(Locations.FORCE_KEEP, null()),
                    spirit_keep_rating = coded_location_ratings.get(Locations.SPIRIT_KEEP, null()),
                    magic_keep_rating = coded_location_ratings.get(Locations.MAGIC_KEEP, null()),
                    void_keep_rating = coded_location_ratings.get(Locations.VOID_KEEP, null()),
                    magma_dragon_rating = coded_location_ratings.get(Locations.MAGMA_DRAGON, null()),
                    frost_spider_rating = coded_location_ratings.get(Locations.FROST_SPIDER, null()),
                    nether_spider_rating = coded_location_ratings.get(Locations.NETHER_SPIDER, null()),
                    scarab_king_rating = coded_location_ratings.get(Locations.SCARAB_KING, null()),
                    eternal_dragon_rating = coded_location_ratings.get(Locations.ETERNAL_DRAGON, null()),
                    celestial_griffin_rating = coded_location_ratings.get(Locations.CELESTIAL_GRIFFIN, null()),
                    dreadhorn_rating = coded_location_ratings.get(Locations.DREADHORN, null()),
                    dark_fae_rating = coded_location_ratings.get(Locations.DARK_FAE, null()),
        )

        existing_rating = session.query(cls).filter_by(champion_id=champion_id, source=data_source).first()

        # If this rating (champion and source) does not exist, add it. If it does exist, get the rating's id and
        # assign it to the newly created one, lthem perform a merge to catch any changes in the source
        if existing_rating is not None:
            rating.id = existing_rating.id
        
        session.merge(rating)
