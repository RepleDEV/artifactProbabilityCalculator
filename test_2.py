from itertools import combinations
from main import main
import json

# Importing files
file_name = "file_2.json"

with open(f"./webscraper/{file_name}", 'r') as f:
    file = json.load(f)

#! OTHER FUNCTIONS
def checkDuplicates(arr):
    sortedArray = arr.copy()
    sortedArray.sort()

    lastElement = sortedArray[0]

    for i in range(1, len(arr)):
        if (sortedArray[i] == lastElement):
            return True
        lastElement = sortedArray[i]
    
    return False

def removeDuplicates(arr):
    seenElements = []

    for i in range(len(arr)):
        element = arr[i]

        if (element not in seenElements):
            seenElements.append(element)

    return seenElements

def getAllCombinations(values, combination_num=4):
    combination = [0] * combination_num
    combinations = [combination.copy()]

    for n in range(len(values)**len(combination)):
        for i in range(len(combination) -1, -1, - 1):
            combination[i] += 1

            if combination[i] == len(values):
                combination[i] = 0
            else:
                if (combination not in combinations):
                    combinations.append(combination.copy())
                break


    filteredCombinations = list(filter(lambda x: not checkDuplicates(x), combinations))

    for i in range(len(filteredCombinations)):
        filteredCombinations[i].sort()

    filteredCombinations = removeDuplicates(filteredCombinations)

    return list(map(lambda x: list(map(lambda y: values[y], x)), filteredCombinations))


########################################
full_chance = 0

arti_types = list(file["subStats"].keys())

for i in range(len(arti_types)):
    arti_type = arti_types[i]
    mainStats = list(file["mainStats"][arti_type].keys())

    for j in range(len(mainStats)):
        mainStat = mainStats[j]

        # substatCombinations = getAllCombinations(subStats, 4)

        if (i < 2):
            subStats = list(file["subStats"][arti_type].keys())
            mainStat = ""
        else:
            mainStat_subStat = mainStat

            if "DMG Bonus%" in mainStat:
                mainStat_subStat = "Elm_Phys_Bonus"

            subStats = list(file["subStats"][arti_type][mainStat_subStat].keys())

        substatCombinations = combinations(subStats, 4)
        substatCombinations = list(map(lambda x: list(x), substatCombinations))

        for k in range(len(substatCombinations)):
            substatCombination = substatCombinations[k]

            full_chance += main(arti_type, substatCombination[0], substatCombination[1], substatCombination[2], substatCombination[3], main_stat=mainStat, full_substats=True, full_substats_probabilities=False, type_probability=True)


print(full_chance)
