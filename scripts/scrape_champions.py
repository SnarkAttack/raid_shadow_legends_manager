from bs4 import BeautifulSoup
import requests
from rsl_manager.db_objs import Champion
from rsl_manager.enums import Affinities, Factions, Roles, Rarities
import re
from rsl_manager.db_objs import engine
from rsl_manager.db_objs.utilities import session_managed

def scrape_all_champions():

    r = requests.get('https://ayumilove.net/raid-shadow-legends-list-of-champions-by-ranking/')
    soup  = BeautifulSoup(r.content, 'html.parser')
    entry = soup.find(class_='entry-content')
    tier_sections = entry.find_all(text=re.compile('^[SABCF] Rank \| (Common|Uncommon|Rare|Epic|Legendary) Champion'))

    champ_and_info = []

    for sec in tier_sections:
        champs_in_tier = sec.parent.find_next_sibling('ul').find_all('li')
        for champ in champs_in_tier:
            space_split = champ.text.split(' ')
            champ_name = ' '.join(space_split[:-1])
            champ_data = space_split[-1]
            champ_and_info.append((champ_name, champ_data))

    return champ_and_info

@session_managed(engine)
def store_all_champions(session, champ_and_info):

    for champ_name, champ_info in champ_and_info:


        affinity = Affinities.from_code(champ_info[6])
        faction = Factions.from_code(champ_info[1:3])
        role = Roles.from_code(champ_info[5])
        rarity = Rarities.from_code(champ_info[4])

        champ = Champion(
            name=champ_name,
            affinity=affinity,
            faction=faction,
            role=role,
            rarity=rarity
        )

        existing_champ = session.query(Champion).filter_by(name=champ_name).first()

        if existing_champ is not None:
            champ.id = existing_champ.id

        session.merge(champ)

    session.commit()

def main():
    champ_and_info = scrape_all_champions()
    store_all_champions(champ_and_info)

if __name__ == '__main__':
    main()
