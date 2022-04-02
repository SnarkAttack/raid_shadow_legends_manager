from enum import IntEnum, auto
from sre_constants import MAGIC

class NamedIntEnum(IntEnum):

    @classmethod
    def get_enum_from_name(cls, name):
        upper_name = name.upper()
        for enum_name in vars(cls):
            if enum_name == upper_name:
                return cls[enum_name]
        raise ValueError(f"No option detected in {cls.__name__} with the name {name}")

    @classmethod
    def get_valid_enums(cls):
        return [e for e in cls if e.name != 'NONE']


class Affinities(NamedIntEnum):
    NONE = 0
    FORCE = auto()
    SPIRIT = auto()
    MAGIC = auto()
    VOID = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'F': cls.FORCE,
            'S': cls.SPIRIT,
            'M': cls.MAGIC,
            'V': cls.VOID
        }

        if code in code_dict.keys():
            return code_dict[code]
        
        raise ValueError(f"No affinity found for code {code}")

class Factions(NamedIntEnum):
    NONE = 0
    BANNER_LORDS = auto()
    HIGH_ELVES = auto()
    SACRED_ORDER = auto()
    BARBARIANS = auto()
    OGRYN_TRIBES = auto()
    LIZARDMEN = auto()
    SKINWALKERS = auto()
    ORCS = auto()
    DEMONSPAWN = auto()
    UNDEAD_HORDES = auto()
    DARK_ELVES = auto()
    KNIGHTS_REVENANT = auto()
    DWARVES = auto()
    SHADOWKIN = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'BL': cls.BANNER_LORDS,
            'HE': cls.HIGH_ELVES,
            'SO': cls.SACRED_ORDER,
            'BA': cls.BARBARIANS,
            'OT': cls.OGRYN_TRIBES,
            'LZ': cls.LIZARDMEN,
            'SW': cls.SKINWALKERS,
            'OR': cls.ORCS,
            'DS': cls.DEMONSPAWN,
            'UH': cls.UNDEAD_HORDES,
            'DE': cls.DARK_ELVES,
            'KR': cls.KNIGHTS_REVENANT,
            'DW': cls.DWARVES,
            'SK': cls.SHADOWKIN
        }

        if code in code_dict.keys():
            return code_dict[code]
        
        raise ValueError(f"No faction found for code {code}")

class Roles(NamedIntEnum):
    NONE = 0
    ATTACK = auto()
    DEFENSE = auto()
    HP = auto()
    SUPPORT = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'A': cls.ATTACK,
            'D': cls.DEFENSE,
            'H': cls.HP,
            'S': cls.SUPPORT
        }
        
        if code in code_dict.keys():
            return code_dict[code]

        raise ValueError(f"No role found for code {code}")

class Rarities(NamedIntEnum):
    NONE = 0
    COMMON = auto()
    UNCOMMON = auto()
    RARE = auto()
    EPIC = auto()
    LEGENDARY = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'L': cls.LEGENDARY,
            'E': cls.EPIC,
            'R': cls.RARE,
            'U': cls.UNCOMMON,
            'C': cls.COMMON
        }

        if code in code_dict.keys():
            return code_dict[code]

        raise ValueError(f"No rarity found for code {code}")

class DataSources(NamedIntEnum):
    NONE = 0
    AYUMILOVE = auto()
    HELL_HADES = auto()
    RAID_CODEX = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'AyumiLoveParser': cls.AYUMILOVE,
            'HellHadesParser': cls.HELL_HADES,
            'RaidCodexParser': cls.RAID_CODEX
        }

        if code in code_dict.keys():
            return code_dict[code]

        raise ValueError(f"No rarity found for code {code}")



class Locations(NamedIntEnum):
    NONE = 0
    CAMPAIGN = auto()
    ARENA_ATK = auto()
    ARENA_DEF = auto()
    CLAN_BOSS = auto()
    FACTION_WARS = auto()
    MINOTAUR = auto()
    SPIDER = auto()
    FIRE_KNIGHT = auto()
    DRAGON = auto()
    ICE_GOLEM = auto()
    ARCANE_KEEP = auto()
    VOID_KEEP = auto()
    FORCE_KEEP = auto()
    SPIRIT_KEEP = auto()
    MAGIC_KEEP = auto()
    DOOM_TOWER_WAVES = auto()
    MAGMA_DRAGON = auto()
    NETHER_SPIDER = auto()
    FROST_SPIDER = auto()
    SCARAB_KING = auto()
    CELESTIAL_GRIFFIN = auto()
    ETERNAL_DRAGON = auto()
    DREADHORN = auto()
    DARK_FAE = auto()

    @classmethod
    def from_code(cls, code):

        code_dict = {
            'Campaign': cls.CAMPAIGN,
            'Arena Offense': cls.ARENA_ATK,
            'Arena Defense': cls.ARENA_DEF,
            'Clan Boss': cls.CLAN_BOSS,
            'Faction Wars': cls.FACTION_WARS,
            'Minotaur': cls.MINOTAUR,
            'Spider': cls.SPIDER,
            'Fire Knight': cls.FIRE_KNIGHT,
            'Dragon': cls.DRAGON,
            'Ice Golem': cls.ICE_GOLEM,
            'Arcane Keep': cls.ARCANE_KEEP,
            'Void Keep': cls.VOID_KEEP,
            'Force Keep': cls.FORCE_KEEP,
            'Spirit Keep': cls.SPIRIT_KEEP,
            'Magic Keep':cls. MAGIC_KEEP,
            'Floors': cls.DOOM_TOWER_WAVES,
            'Magma Dragon': cls.MAGMA_DRAGON,
            'Nether Spider': cls.NETHER_SPIDER,
            'Frost Spider': cls.FROST_SPIDER,
            'Scarab King': cls.SCARAB_KING,
            'Celestial Griffin': cls.CELESTIAL_GRIFFIN,
            'Eternal Dragon': cls.ETERNAL_DRAGON,
            'Dreadhorn': cls.DREADHORN,
            'Dark Fae': cls.DARK_FAE,
            'Arena (Offensive)': cls.ARENA_ATK,
            'Arena (Defensive)': cls.ARENA_DEF,
            # Don't care about this at all, so assign to None
            'Clan boss (Without T6 mastery)': cls.NONE,
            'Clan boss (With T6 mastery)': cls.CLAN_BOSS,
            'Ice Golem\u2019s Peak': cls.ICE_GOLEM,
            'Dragon\u2019s Lair': cls.DRAGON,
            'Spider\u2019s Den': cls.SPIDER,
            'Fire Knight\u2019s Castle': cls.FIRE_KNIGHT,
            'Minotaur\u2019s Labyrinth': cls.MINOTAUR,
            'Arena Def': cls.ARENA_DEF,
            'Arena Atk': cls.ARENA_ATK,
            'Doom Tower Waves': cls.DOOM_TOWER_WAVES,
        }

        if code in code_dict.keys():
            return code_dict[code]

        raise ValueError(f"No rarity found for code {code}")

class ArtifactTypes(NamedIntEnum):
    NONE = 0
    WEAPON = auto()
    HELMET = auto()
    SHIELD = auto()
    GAUNTLETS = auto()
    CHESTPLATE = auto()
    BOOTS = auto()
    RING = auto()
    AMULET = auto()
    BANNER = auto()


class ArtifactSets(NamedIntEnum):
    NONE = 0
    LIFE = auto()
    DEFENSE = auto()
    RESISTANCE = auto()
    OFFENSE = auto()
    CRITICAL_RATE = auto()
    RETALIATION = auto()
    REFLEX = auto()
    CURSED = auto()
    TAUNTING = auto()
    FROST = auto()
    TOXIC = auto()
    DAZE = auto()
    AVENGING = auto()
    STALWART = auto()
    ACCURACY = auto()
    SPEED = auto()
    LIFESTEAL = auto()
    DESTROY = auto()
    FRENZY = auto()
    STUN = auto()
    IMMUNITY = auto()
    SAVAGE = auto()
    REGENERATION = auto()
    FURY = auto()
    CURING = auto()
    CRITICAL_DAMAGE = auto()
    SHIELD = auto()
    CRUEL = auto()
    IMMORTAL = auto()
    DIVINE_LIFE = auto()
    DIVINE_CRITICAL_RATE = auto()
    DIVINE_OFFENSE = auto()
    DIVINE_SPEED = auto()
    SWIFT_PARRY = auto()
    DEFLECTION = auto()
    RESILIENCE = auto()
    PERCEPTION = auto()
    FATAL = auto()
    AFFINITYBREAKER = auto()
    UNTOUCHABLE = auto()
    FROSTBITE = auto()
    BLOODTHIRST = auto()
    GUARDIAN = auto()
    RELENTLESS = auto()
    FORTITUDE = auto()
    LETHAL = auto()
    STONE_SKIN = auto()
    PROTECTION = auto()