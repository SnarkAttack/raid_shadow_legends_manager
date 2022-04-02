import sys
from turtle import RawTurtle, color
import matplotlib.pyplot as plt
from enum import Enum, auto
from rsl_manager.enums import Rarities
from math import comb

DOUBLE_ANCIENT = '-ea'
DOUBLE_VOID = '-ev'
DOUBLE_SACRED = '-es'
OTHER = ' '

class Shards(Enum):
    MYSTERY = 'm'
    ANCIENT = 'a'
    VOID = 'v'
    SACRED = 's'

    @classmethod
    def enum_from_code(cls, code):
        for e in cls:
            if e.value == code:
                return e

shard_odds_dict = {
    Shards.MYSTERY: {
        OTHER: {
            Rarities.COMMON: 0.742,
            Rarities.UNCOMMON: 0.244,
            Rarities.RARE: 0.014,
            Rarities.EPIC: 0,
            Rarities.LEGENDARY: 0
        }
    },
    Shards.ANCIENT: {
        DOUBLE_ANCIENT: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0.83,
            Rarities.EPIC: 0.16,
            Rarities.LEGENDARY: 0.01
        },
        OTHER: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0.915,
            Rarities.EPIC: 0.08,
            Rarities.LEGENDARY: 0.005
        }
    },
    Shards.VOID: {
        DOUBLE_VOID: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0.83,
            Rarities.EPIC: 0.16,
            Rarities.LEGENDARY: 0.01
        },
        OTHER: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0.915,
            Rarities.EPIC: 0.08,
            Rarities.LEGENDARY: 0.005
        }
    },
    Shards.SACRED: {
        DOUBLE_SACRED: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0,
            Rarities.EPIC: 0.88,
            Rarities.LEGENDARY: 0.12
        },
        OTHER: {
            Rarities.COMMON: 0,
            Rarities.UNCOMMON: 0,
            Rarities.RARE: 0,
            Rarities.EPIC: 0.94,
            Rarities.LEGENDARY: 0.06
        }
    }
}

def get_all_combos(num_shards, num_possibilities):

    if num_possibilities == 2:
        return [(x, num_shards-x) for x in range(num_shards+1)]
    elif num_possibilities == 3:
        return[(x, y, num_shards-x-y) for x in range(num_shards+1) for y in range(num_shards-x+1)]
    else:
        raise ValueError("Impossible number of output classes")

def get_shard_odds(shard_type, event):

    shard_type_odds = shard_odds_dict[shard_type]

    if event in shard_type_odds.keys():
        event_odds = shard_type_odds[event]
    else:
        event_odds = shard_type_odds[OTHER]

    return  {k: v for k, v in event_odds.items() if v != 0}

def calculate_shard_odds(shard_type, num_shards, event):
    
    shard_odds = get_shard_odds(shard_type, event)
    combos = get_all_combos(num_shards, len(shard_odds))
    odds_values = list(shard_odds.values())
    vals = []
    for combo in combos:
        val = 1
        for idx, num_type_shards in enumerate(combo):
            val *= pow(odds_values[idx], num_type_shards) * comb(sum(combo[idx:]), combo[idx])
        vals.append(round(val, 8))

    combo_odds = list(zip(combos, vals))

    return list(shard_odds.keys()), combo_odds

def get_rarity_color(rarity):
    if rarity == Rarities.COMMON:
        return 'grey'
    elif rarity == Rarities.UNCOMMON:
        return 'green'
    elif rarity == Rarities.RARE:
        return 'blue'
    elif rarity == Rarities.EPIC:
        return 'purple'
    elif rarity == Rarities.LEGENDARY:
        return 'gold'
    else:
        raise ValueError("Invalid rarity")

def plot_shard_odds(num_possibilities, shard_type, shards, combo_odds):
    
    fig, ax = plt.subplots()

    biggest_combos = [x[0] for x in sorted(combo_odds, key=lambda x: x[1])[-num_possibilities:]]

    combo_odds = [combo_odd for combo_odd in combo_odds if combo_odd[0] in biggest_combos and round(100*combo_odd[1], 2) != 0]

    num_possibilities = min(num_possibilities, len(combo_odds))

    combo_odds.sort(key=lambda x: x[1])

    combos, odds = zip(*combo_odds)

    total_chance_shown = sum(odds)

    labels = [f"{combo}\n{round(100*odds, 2)}" for combo, odds in combo_odds]

    last_height = [0] * num_possibilities
    for j in range(len(shards)):

        rarity_height = [combo[j]*odds[idx]/sum(combo) for idx, combo in enumerate(combos)]
        ax.bar(labels, rarity_height, width=.5, color=get_rarity_color(shards[j]), bottom=last_height)
        last_height = [sum(x) for x in zip(last_height, rarity_height)]

    plt.title(f"Top {num_possibilities} possibilities for {sum(combos[0])} {shard_type.name.title()} shards (~{round(100*total_chance_shown, 2)}% shown)")
    plt.show()
    

def parse_args():

    if len(sys.argv) < 4:
        raise ValueError("Missing arguments: arguments should be 'shard-odds <shard_num> <num_possibilities_to_display> <shard_type: m,a,v,s> <optional event type: -a,-s,-v>'")
    elif len(sys.argv) >= 4:
        num_shards = int(sys.argv[1])
        num_possibilities = int(sys.argv[2])
        shard_type = Shards.enum_from_code(sys.argv[3])
        event_type = None
        opt_args = sys.argv[4:]

        if DOUBLE_ANCIENT in opt_args:
            event_type = DOUBLE_ANCIENT
        elif DOUBLE_VOID in opt_args:
            event_type = DOUBLE_VOID
        elif DOUBLE_SACRED in opt_args:
            event_type = DOUBLE_SACRED
        else:
            raise ValueError("Unknown optional args")

        return (num_shards, num_possibilities, shard_type, event_type)

def main():
    num_shards, num_possibilities, shard_type, event = parse_args()
    shards, combo_odds = calculate_shard_odds(shard_type, num_shards, event)
    for idx, shard_type in enumerate(shards):
        print(f"Odds of at least 1 {shard_type.name.title()}: ~{round(100*sum([combo_odd[1] for combo_odd in combo_odds if combo_odd[0][idx] > 0]), 2)}%")
    plot_shard_odds(num_possibilities, shard_type, shards, combo_odds)
    # print(sum([combo_odd[1] for combo_odd in combo_odds if combo_odd[0][-1] > 0]))
