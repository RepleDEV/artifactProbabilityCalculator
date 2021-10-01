from main import main
import json

# Importing files
file_name = "file_2.json"

with open(f"./webscraper/{file_name}", 'r') as f:
    file = json.load(f)

full_chance = 0

arti_types = list(file["subStats"].keys())
for i in range(len(arti_types)):
    print(f"Arti type: {i + 1}")

    # If feather / flower
    if (i < 2):
        arti_type = arti_types[i]
        sub_stats = file['subStats'][arti_type]

        sub_stats_keys = list(sub_stats.keys())

        combination = sub_stats_keys[:4]
        combinations = [combination.copy()]

        for k in range(len(combination)):
            currCombination = combination[k]
            for l in range(len(sub_stats_keys)):
                substatIndex = (sub_stats_keys.index(currCombination) + l) % len(sub_stats_keys)

                if not sub_stats_keys[substatIndex] in combination:
                    combination[k] = sub_stats_keys[substatIndex]

                    combinations.append(combination.copy())
        
        for k in range(len(combinations)):
            print(f"Combination: {k + 1}")

            full_chance += main(arti_type, combination[0], combination[1], combination[2], combination[3], full_substats=True)
    else:
        arti_type = arti_types[i]
        main_stats = list(file["mainStats"][arti_type].keys())
        for j in range(len(main_stats)):
            main_stat = main_stats[j]
            main_stat_substats = main_stat

            if "DMG Bonus%" in main_stat_substats:
                main_stat_substats = "Elm_Phys_Bonus"

            sub_stats = file['subStats'][arti_type][main_stat_substats]

            sub_stats_keys = list(sub_stats.keys())

            combination = sub_stats_keys[:4]
            combinations = [combination.copy()]

            for k in range(len(combination)):
                currCombination = combination[k]
                for l in range(len(sub_stats_keys)):
                    substatIndex = (sub_stats_keys.index(currCombination) + l) % len(sub_stats_keys)

                    if not sub_stats_keys[substatIndex] in combination:
                        combination[k] = sub_stats_keys[substatIndex]

                        combinations.append(combination.copy())
            
            for k in range(len(combinations)):
                print(f"Combination: {k + 1}")

                full_chance += main(arti_type, combination[0], combination[1], combination[2], combination[3], main_stat, True)
            

print(full_chance)


"""
VALUES = [1, 2, 3, 4]

combination = [1, 1]
combinations = [combination.copy()]

for i in range(len(combination)):
    currCombination = combination[i]
    for j in range(len(VALUES)):
        valueIndex = (VALUES.index(currCombination) + j) % len(VALUES)

        #print(1, combinations, i, j, valueIndex)

        if (VALUES[valueIndex] is not currCombination):
            combination[i] = VALUES[valueIndex]
            #print(2, combinations, i, j, valueIndex)
            combinations.append(combination.copy())
            #print(3, combinations, i, j, valueIndex)
        #print(4, combinations, i, j, valueIndex)

print(combinations);

# print(len(combinations))
# print(combinations)
"""