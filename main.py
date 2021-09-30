import json

# Importing files
path = "C:/Users/Sentro/Downloads/"
file_name = "file.json"

with open(f"{path}{file_name}", 'r') as f:
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
    # Step 1, set probability
    current_probability = 1
    # Step 2, type probability (since 1 domain artifact has a chance of getting 2 artifacts type)
    current_probability /= 2
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
        chances = sub_stats[arti_type][main_stat]
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


# Below is just to retrieve user's inputs

user_inputs = []
has_mainstats = False
has_substats = False

user_input = input("Enter your main artifact: ")
user_inputs.append(user_input)
if user_input in genshin_artifacts[:2]:
    has_mainstats = True
    user_input = input("Enter main stats: ")
has_substats = input('Does your artifact have full substats? [Y/N]: ').lower()
has_substats = True if has_substats == 'y' else False  # If have substats, is True
rng = 4 if has_substats else 3  # Thus, it'd have 4 substats if True.
for i in range(rng):
    user_artifacts = input(f"Enter your substat #{i + 1}: ")  # Enter each substats
    user_inputs.append(user_artifacts)
if has_mainstats:
    user_inputs.append(user_input)
#print(user_inputs)

mainstat = user_inputs[5] if has_mainstats else ''
sub4 = user_inputs[4] if has_substats else ''
genshin_chance = round(main(user_inputs[0], user_inputs[1], user_inputs[2], user_inputs[3],
                            main_stat=mainstat, substat_4=sub4, full_substats=has_substats) * 100_000)

print(f"It is estimated of 1 / {round((100_000 / genshin_chance))} chance on getting your artifact.")
