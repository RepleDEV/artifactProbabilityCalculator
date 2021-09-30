def main(artifact_type, main_stat, substat_1, substat_2, substat_3, substat_4, full_substats=False):
    current_probability = 1
    # Step 1, set probability
    current_probability /= 2
    # Step 2, type probability
    current_probability /= 5
    # Step 3, main stat probability
    
    # Step 4, Full substats
    if (full_substats):
        current_probability /= 0.25
    else:
        current_probability /= 0.75
    # Step 5, Substats


    return current_probability*100