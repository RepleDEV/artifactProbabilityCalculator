
import json
from fractions import Fraction

with open(r'C:\Users\Sentro\Downloads\file.json', 'r') as f:
    file = json.load(f)

genshin_artifacts = ['sands', 'goblet', 'circlet', 'flower', 'feather'] # flower is always HP, plume is always ATK

main_stat = file['mainStats']
sub_stats = file['subStats']

# Probabilities: list of numbers
def rescale_probabilities(probabilities, index):
    probabilities.pop(index)
    sum_of_probabilities = sum(probabilities)
    scaling = 100 / sum_of_probabilities

    return list(map(lambda x: x * scaling, probabilities))

def main(arti_type, main_stat, substat_1, substat_2, substat_3, substat_4, full_substats=False):
    # Step 1, set probability
    current_probability = 1
    # Step 2, type probability
    current_probability /= 2
    # Step 3, main stat probability
    if main_stat in genshin_artifacts[:2]: # if flower / feather
        current_probability *= (main_stat[arti_type][main_stat] / 100)

    # Step 4, Full substats
    if (full_substats):
        current_probability *= 0.25
    else:
        current_probability *= 0.75

    # Step 5, Substats
    #if not full_substats:
    if main_stat not in genshin_artifacts[:2]: # Because flower and feather main stats dont influence substats
        chances = sub_stats[arti_type]
    else:
        chances = sub_stats[arti_type][main_stat]

    chances_keys = list(chances.keys())
    chances_values = list(chances.values())
    substats = [substat_1, substat_2, substat_3, substat_4]
    for stats in substats:
        chance = chances[stats]

        indice = chances_keys.index(stats)
        current_probability *= chance / 100

        chances_values = rescale_probabilities(chances_values, indice)

        chances_keys.pop(indice)

    return current_probability * 100


genshin_chance = round(main('feather', 'ATK', 'HP%', 'CRIT Rate%', 'CRIT DMG%', 'ATK%', True) * 100_000)

final_chance = Fraction(genshin_chance, 100_000)
print(f"{final_chance} chance on getting the artifact you want.")
