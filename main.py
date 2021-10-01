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

# Main function
def main(arti_type, substat_1, substat_2, substat_3, substat_4='', main_stat='', full_substats=False):
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
    has_mainstats = True if main_stat != '' else False

    current_probability = 1

    # Step 1, Artifact set probability
    current_probability /= 2
    # Step 2, type probability (since 1 domain artifact has a chance of getting 2 artifacts type)
    current_probability /= 5
    # Step 3, main stat probability, if artifact has main_stat:
    if has_mainstats:
        current_probability *= (main_stats[arti_type][main_stat] / 100)
    
    # Step 4, if full substats
    if (full_substats):
        current_probability *= 0.25
    else:
        current_probability *= 0.75

    # Step 5, Substats
    if has_mainstats:
        # List of numbers of substats
        main_stat_substats = main_stat
        
        if "DMG Bonus%" in main_stat_substats:
                    main_stat_substats = "Elm_Phys_Bonus"

        chances = sub_stats[arti_type][main_stat_substats]
    else:
        chances = sub_stats[arti_type]
    chances_keys = list(chances.keys())
    chances_values = list(chances.values())
    if full_substats:
        # Returns ['HP', 'HP%', 'DEF', 'ATK]
        substats = [substat_1, substat_2, substat_3, substat_4]
    else:
        # Returns ['HP', 'DEF', 'ATK]
        substats = [substat_1, substat_2, substat_3]

    for stats in substats:
        chance = chances[stats]
        # Finds the index of the chance of getting that substats
        indice = chances_keys.index(stats)
        current_probability *= chance / 100
        # Rescaling the list
        chances_values = rescale_probabilities(chances_values, indice)
        # Removes from the chances of having that substats again because substats are unrepeatable.
        chances_keys.pop(indice)
    return current_probability * 100
