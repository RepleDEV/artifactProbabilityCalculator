from functools import reduce
from itertools import permutations
import json

# Importing files
file_name = "file_2.json"

with open(f"./webscraper/{file_name}", 'r') as f:
    file = json.load(f)

# Flower artifact mainstats is always HP, while feather is always ATK
genshin_artifacts = ['sands', 'goblet', 'circlet', 'flower', 'feather']

main_stats = file['mainStats']
sub_stats = file['subStats']

# Probabilities: returns a list of numbers, scaled version of probabilities
def rescale_probabilities(probabilities, index):
    probabilities.pop(index)
    sum_of_probabilities = sum(probabilities)
    scaling = 100 / sum_of_probabilities
    return list(map(lambda x: x * scaling, probabilities))

def calculate_substat_probabilities(arr):
    probabilities = arr.copy()

    for i in range(1, len(probabilities)):
            for j in range(len(probabilities[i:])):
                probabilities[i + j] *= (1/(1 - probabilities[i - 1]))
                probabilities[i + j] = round(probabilities[i + j], 5)

    return probabilities
# Main function
def main(
    arti_type, 
    substat_1, 
    substat_2, 
    substat_3, 
    substat_4='', 
    main_stat='', 
    full_substats=False, 
    full_substats_probabilities=True,
    any_order=True,
    set_probability=False,
    type_probability=False
):
    """
    :str arti_type: What artifact wants to be calculated (ex: sands)
    :str substat_1: substat number 1 (ex: HP)
    :str substat_2: substat number 2 (ex: ATK)
    :str substat_3: substat number 3 (ex: DEF)
    :str main_stat: optional, the mainstat that you have (ex: ATK%)
    :str substat_4: optional, substat number 4 (ex: HP)
    :bool full_substats: whether the artifact has all 4 substats.
    :return: a float number of the probability (ex: 0.00084738)
    PS: Case sensitive.
    """
    has_mainstats = main_stat != ''

    current_probability = 1

    # Step 1, Artifact set probability
    if (set_probability):
        current_probability *= 1/2
    # Step 2, type probability (since 1 domain artifact has a chance of getting 2 artifacts type)
    if (type_probability):
        current_probability *= 1/5
    # Step 3, main stat probability, if artifact has main_stat:

    if has_mainstats:
        current_probability *= (main_stats[arti_type][main_stat] / 100)
    

    # Step 4, if full substats
    if (full_substats_probabilities):
        if (full_substats):
            current_probability *= 1/4
        else:
            current_probability *= 3/4

    current_probability_before_substats = current_probability

    # Step 5, Substats
    if has_mainstats:
        # List of numbers of substats
        main_stat_substats = main_stat
        
        if "DMG Bonus%" in main_stat_substats:
                    main_stat_substats = "Elm_Phys_Bonus"

        chances = sub_stats[arti_type][main_stat_substats]
    else:
        chances = sub_stats[arti_type]

    if full_substats:
        # Returns ['HP', 'HP%', 'DEF', 'ATK]
        substats = [substat_1, substat_2, substat_3, substat_4]
    else:
        # Returns ['HP', 'DEF', 'ATK]
        substats = [substat_1, substat_2, substat_3]

    chances_substats = list(map(lambda x: chances[x] / 100,substats))

    if (any_order):
        # TODO: make a better algorithm KKonaW
        chances_substats_perms = list(permutations(chances_substats))
        # [tuple] to [list]
        chances_substats_perms = list(map(lambda x: list(x), chances_substats_perms))

        substat_chances = 0

        for i in range(len(chances_substats_perms)):
            chances_substats = chances_substats_perms[i]

            calculated_chances = calculate_substat_probabilities(chances_substats)
            substat_chances += reduce(lambda a, b: a*b,list(map(lambda x: x, calculated_chances)))

        current_probability *= substat_chances
    else:
        calculated_chances = calculate_substat_probabilities(chances_substats)
        current_probability *= reduce(lambda a, b: a*b,list(map(lambda x: x, calculated_chances)))

    return round(current_probability * 100, 5)


print(main("feather", "HP%", "CRIT Rate%", "CRIT DMG%", "ATK%", full_substats=True, any_order=True, full_substats_probabilities=False))