from main import main

# Flower artifact mainstats is always HP, while feather is always ATK
genshin_artifacts = ['sands', 'goblet', 'circlet', 'flower', 'feather']

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