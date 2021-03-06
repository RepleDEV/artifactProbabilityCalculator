from functools import reduce
from itertools import permutations, combinations
from numpy import array, sum
import json

# Importing files
file_name = "file_2.json"

with open(f"./webscraper/{file_name}", 'r') as f:
    file = json.load(f)

main_stats = file['mainStats']
sub_stats = file['subStats']

# Calculate scaled probabilities for len(arr) substats
def scale_substat_probabilities(arr):
    probabilities = arr.copy()

    for i in range(1, len(probabilities)):
            for j in range(len(probabilities[i:])):
                probabilities[i + j] *= (1/(1 - probabilities[i - 1]))
                probabilities[i + j] = round(probabilities[i + j], 5)

    return probabilities

# Substat probability calculator
# TODO: Make this easier to read :)
def calculate_substat_probability(desired_substats, all_substats, any_order=True):
    substat_combinations = []

    if len(substat_combinations) < 4:
        # all_substats - desired_substats
        filteredSubstats = list(filter(lambda x: x not in desired_substats, all_substats))
        fill_number = 4 - len(desired_substats)

        fill_combinations = combinations(filteredSubstats, fill_number)

        for i, v in enumerate(fill_combinations):
            substat_combinations.append(desired_substats + v)
    else:
        substat_combinations[0] = desired_substats.copy()

    # If any order is true
    if any_order:
        # Get all permutations of all combinations.
        substat_combinations = list(permutations(substat_combinations))
    # Scale probabilities of all combinations
    substat_combinations = list(map(lambda x: reduce(lambda a, b: a * b, scale_substat_probabilities(list(x))), substat_combinations))
    # Return sum
    return float(sum(array(substat_combinations)))

# Main function
def main(
    arti_type,
    substats=[],
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
    ## Constants
    HAS_MAINSTATS = main_stat != ''
    SET_PROBABILITY = 1/2
    TYPE_PROBABILITY = 1/5

    # Will be final result
    current_probability = 1

    # Step 1, Artifact set probability
    if (set_probability):
        current_probability *= SET_PROBABILITY
    # Step 2, type probability (since 1 domain artifact has a chance of getting 2 artifacts type)
    if (type_probability):
        current_probability *= TYPE_PROBABILITY

    # Also, define substat_distribution variable for later
    substat_distribution = sub_stats[arti_type]

    # Step 3, check if artifact is not flower or feather.
    if arti_type != "flower" and arti_type != "feather":
        # If it is, main_stat parameter must be filled because the substat distributions
        # are dependant on the main_stat parameter

        if HAS_MAINSTATS:
            current_probability *= (main_stats[arti_type][main_stat] / 100)

            #! Substat JSON key workaround
            # Copy main_stat variable
            main_stat_substats = main_stat
                
            # This checks if main_stat is {Element/Physical} Bonus%
            if "DMG Bonus%" in main_stat_substats:
                # Then replaces it with: (cuz {Element/Physical} Bonus% main stat artifacts have the same sub stat distributions)
                # And is grouped together in the JSON file
                # Thus
                main_stat_substats = "Elm_Phys_Bonus"
            #! Substat JSON key workaround

            # re-define substat_distribution variable for later
            substat_distribution = sub_stats[arti_type][main_stat_substats]
        else:
            # Raise error >:)
            raise ValueError("Parameter arti_type is not \"flower\" or \"feather\".\nParameter main_stat must be filled.")
    

    # # Check if probability for full substats is enabled
    if (full_substats_probabilities):
        # If so, (Step 4) check if full (4) substats parameter
        if (full_substats):
            current_probability *= 1/5
        else:
            current_probability *= 4/5

    # substats = [substat_1, substat_2, substat_3, substat_4]

    # Rescale percentage to decimal (0...100) to (0...1)
    chances_substats = list(map(lambda x: substat_distribution[x] / 100, substats))
    substat_chances = calculate_substat_probability(chances_substats, sub_stats[arti_type][main_stat],any_order=any_order)

    current_probability *= substat_chances

    # Optional: multiply this by 1.07 cuz from 1 fragile run there's a 7% chance u get 2 artis
    return round(current_probability * 100, 5);


# print(main("goblet", "HP%", "CRIT Rate%", "CRIT DMG%", "Elemental Mastery", main_stat="Pyro DMG Bonus%", full_substats=False, full_substats_probabilities=False, type_probability=True))