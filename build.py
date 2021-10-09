# Gather all possible outcome's probabilities, put it all into 1 file :smile:
from itertools import combinations
from main import main
import json

# Importing files
file_name = "file_2.json"

with open(f"./webscraper/{file_name}", 'r') as f:
    file = json.load(f)

# Empty output dict
output = {}

def build(filename):

    arti_types = list(file["subStats"].keys())

    for i in range(len(arti_types)):
        arti_type = arti_types[i]
        mainStats = list(file["mainStats"][arti_type].keys())

        output[arti_type] = {}

        for j in range(len(mainStats)):
            mainStat = mainStats[j]

            output[arti_type][mainStat] = {}

            # substatCombinations = getAllCombinations(subStats, 4)

            if (i < 2):
                subStats = list(file["subStats"][arti_type].keys())
                newMainStat = ""
            else:
                newMainStat = mainStat
                mainStat_subStat = mainStat

                if "DMG Bonus%" in mainStat:
                    mainStat_subStat = "Elm_Phys_Bonus"

                subStats = list(file["subStats"][arti_type][mainStat_subStat].keys())

            substatCombinations = combinations(subStats, 4)
            substatCombinations = list(map(lambda x: list(x), substatCombinations))

            for k in range(len(substatCombinations)):
                substatCombination = substatCombinations[k]

                probability = main(arti_type, substatCombination[0], substatCombination[1], substatCombination[2], substatCombination[3], main_stat=newMainStat, full_substats=True, full_substats_probabilities=False, type_probability=True)
                probability_semi = main(arti_type, substatCombination[0], substatCombination[1], substatCombination[2], substatCombination[3], main_stat=newMainStat, full_substats=False, full_substats_probabilities=True, type_probability=True)
                probability_full = main(arti_type, substatCombination[0], substatCombination[1], substatCombination[2], substatCombination[3], main_stat=newMainStat, full_substats=True, full_substats_probabilities=True, type_probability=True)

                currentTravel = output[arti_type][mainStat]

                for l in range(len(substatCombination) - 1):
                    substat = substatCombination[l]

                    if substat not in currentTravel:
                        currentTravel[substat] = {}
                    currentTravel = currentTravel[substat]
                        
                currentTravel[substatCombination[-1]] = {
                    "default": probability,
                    "semi": probability_semi,
                    "full": probability_full
                }
build("./build.json")

outputjson = json.dumps(output)

f = open("./build.json", "w")

f.write(outputjson)
f.close()