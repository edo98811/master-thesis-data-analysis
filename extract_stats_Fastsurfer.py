import zipfile
import os
import pandas as pd
import shutil
import csv
import re


def extract_path(filename, base_path):

    subjs_path = []
    for path, subdirs, files in os.walk(base_path):
        if path.split("/")[-1] == 'stats':
            for name in files:
                if name == filename:
                    subjs_path.append(path + "/" + name)

    if not subjs_path:
        return False

    return subjs_path


def stats(subj_paths):
    df_dict = {"subjects": []}

    for n, path in enumerate(subj_paths):
        print("extracting stats for subject " + str(n + 1) + ", path:" + path)

        # saving the subject name
        df_dict["subjects"].append(path.split("/")[-3])

        # opens file and loads it as list of lines
        with open(path, "r") as file:
            data = file.readlines()

        # iterating though the lines
        for i, line in enumerate(data):

            # part 1
            match = re.match(r"^# Measure (\w+).+(\d+ | \d+\.\d+),\s\w+$", line)

            if match:
                # if it's the first iteration it creates the lists, assumes all the files are the same (which should be)
                if not n:
                    df_dict[match.group(1)] = [match.group(2)]
                    print(df_dict)
                else:
                    df_dict[match.group(1)].append(
                        match.group(2))

            # part 2
            if not line.startswith("#"):    # the last table is the only part in which the lines don't start with #
                values = line.strip().split()   # extracts the words and puts them in lists

                if not n:
                    df_dict[values[4] + " volume"] = [values[3]]
                else:
                    df_dict[f"{values[4]} volume"].append(values[3])

    return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    base_path = '/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output_Comparison_AD/'

    # the filename of the stats to extract
    filename = 'aseg.stats'

    subj_paths = extract_path(filename, base_path)
    if subj_paths:
        print("stats file found for " + str(len(subj_paths)) + " subjects")
        stats(subj_paths).to_csv("aseg_AD.csv", index=False)
    else:
        print("no file found")
