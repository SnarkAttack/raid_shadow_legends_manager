import sys
from rsl_manager.web.ratings import AyumiLoveParser, HellHadesParser, RaidCodexParser
from rsl_manager.db_objs import OwnedChampion, Champion, Rating

def get_champ_names(only_owned=False):

    if only_owned:
        champ_names = OwnedChampion.get_all_unique_names()
    else:
        champ_names = Champion.get_all_names()

    return champ_names

def web_fetch_and_save_ratings(only_owned=False):

    raid_codex_parser = RaidCodexParser()
    hell_hades_parser = HellHadesParser()
    ayumilove_parser = AyumiLoveParser()

    parsers = [raid_codex_parser, hell_hades_parser, ayumilove_parser]
    
    champ_names = get_champ_names(only_owned=only_owned)

    rating_results = []
    for champion in champ_names:
        print(champion)
        for parser in parsers:
            try:
                rating_results = parser.parse_champion(champion)
                Rating.from_rating_parser(champion, rating_results, parser.get_site_name())
            except AttributeError as e:
                pass

def main():

    args = {
        'only_owned': True
    }

    if len(sys.argv) > 1:
        args = sys.argv[1:]
    if "-a" in args or "--all" in args:
        args['only_owned'] = False

    web_fetch_and_save_ratings(**args)
