import os
import configparser
from rsl_manager.db_objs import OwnedChampion, engine
from sqlalchemy.orm import Session
from rsl_manager.enums import Factions, Rarities, Locations

config = configparser.ConfigParser()
config.read('config.ini')
output_dir = os.path.join(config['DEFAULT']['OutputDir'], config['RATINGS']['OutputDir'])

def convert_rating_to_num(rating):
    if isinstance(rating, str):
        return 0
    else:
        return rating

def main():

    with Session(engine) as session:

        owned_champions = OwnedChampion.get_all_unique_owned_champions(session)

        # Overall ratings
        with open(os.path.join(output_dir, 'overall_ratings.txt'), 'w') as f:
            named_ratings = [(owned_champion.name, owned_champion.get_overall_rating()) for owned_champion in owned_champions]
            named_ratings.sort(reverse=True, key=lambda x: x[1])
            f.write("Overall Ratings:\n")
            for named_rating in named_ratings:
                f.write(f"  {named_rating[0]}: {named_rating[1]}\n")

        for location in Locations.get_valid_enums():
            with open(os.path.join(output_dir, f'{location.name.lower()}.txt'), 'w') as f:
                location_ratings = [(owned_champion.name, owned_champion.get_location_rating(location)) for owned_champion in owned_champions]
                location_ratings.sort(reverse=True, key=lambda x: convert_rating_to_num(x[1]))
                f.write(f"{location.name.replace('_', ' ').title()} Ratings:\n")
                for location_rating in location_ratings:
                    f.write(f"  {location_rating[0]}: {location_rating[1]}\n")


        # named_ratings.sort(reverse=True, key=lambda x: x[1])
        # fire_knight_ratings.sort(reverse=True, key=lambda x: x[1])

        # print("Ratings by faction:")
        # for faction in Factions:
        #     if faction != Factions.NONE:
        #         print(f"  {faction.name.replace('_', ' ').title()}:")
        #         named_ratings = [(faction_champion.name, faction_champion.get_overall_rating()) for faction_champion in OwnedChampion.get_champions_by_faction(session, faction)]
        #         named_ratings.sort(reverse=True, key=lambda x: x[1])
        #         for named_rating in named_ratings:
        #             print(f"    {named_rating[0]}: {named_rating[1]}")

        # print("Ratings by rarity:")
        # for rarity in sorted(Rarities, reverse=True):
        #     if rarity != Rarities.NONE:
        #         print(f"  {rarity.name.title()}:")
        #         named_ratings = [(rarity_champion.name, rarity_champion.get_overall_rating()) for rarity_champion in OwnedChampion.get_champions_by_rarity(session,  rarity)]
        #         named_ratings.sort(reverse=True, key=lambda x: x[1])
        #         for named_rating in named_ratings:
        #             print(f"    {named_rating[0]}: {named_rating[1]}")



