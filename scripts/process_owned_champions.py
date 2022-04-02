from rsl_manager.db_objs import OwnedChampion
from rsl_manager.db_objs import engine
from rsl_manager.db_objs.utilities import session_managed
import json

def main():
    file_path = 'data/champions.json'
    
    with open(file_path, 'r') as f:
        all_owned_champions = json.load(f)

    for owned_champ_data in all_owned_champions:
        OwnedChampion.champ_from_json(owned_champ_data)


if __name__ == "__main__":
    main()