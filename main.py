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
def calculate_substat_probability(desired_substats, substat_amount=4, any_order=True):
    # 1. Get all combinations for the substats. This returns [desired_substats] when substat_amount == 4
    substat_combinations = list(combinations(list(desired_substats), substat_amount))
    # If any order is true
    if any_order:
        # Get all permutations of all combinations.
        substat_combinations = list(map(lambda x: list(permutations(x)), substat_combinations))
    # Flatten 1+nd array to 1d array w/ numpy
    substat_combinations = list(
        array(
            substat_combinations
        ).flatten()
    )
    # See: https://stackoverflow.com/a/4998460/13160047
    # Group array elements by substat_amount
    substat_combinations = [substat_combinations[n:n+substat_amount] for n in range(0, len(substat_combinations), substat_amount)]
    # Scale probabilities of all combinations
    substat_combinations = list(map(lambda x: reduce(lambda a, b: a * b, scale_substat_probabilities(x)), substat_combinations))
    # Return sum
    return float(sum(array(substat_combinations)))

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
            current_probability *= 1/4
        else:
            current_probability *= 3/4

    substats = [substat_1, substat_2, substat_3, substat_4]

    chances_substats = list(map(lambda x: substat_distribution[x] / 100, substats))
    substat_chances = calculate_substat_probability(chances_substats, substat_amount=4 if full_substats else 3, any_order=any_order)

    current_probability *= substat_chances

    return round(current_probability * 100, 5)


print(main("feather", "HP%", "CRIT Rate%", "CRIT DMG%", "ATK%", full_substats=True, full_substats_probabilities=False))