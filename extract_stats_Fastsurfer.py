import zipfile
import os
import pandas as pd
import shutil
import csv
import re


def extract_path(filename, base_path):
    # all_path = []

    subjs_path = []
    for path, subdirs, files in os.walk(base_path):
        # print(path.split("/"))
        if path.split("/")[-1] == 'stats':
            for name in files:
                # print(path + name)
                # all_path.append(os.path.join(path, name))
                if name == filename:
                    subjs_path.append(path + "/" + name)

    if not subjs_path:
        return False
    # for p in all_path:
    #     if '/stats/' in p:
    #         if filename in p:
    #             subjs_path.append(p)

    return subjs_path


def stats(subj_paths):
    df_dict = {}

    for n, path in enumerate(subj_paths):
        print("extracting stats for subject " + str(n + 1) + ", path:" + path)
        with open(path, "r") as file:
            data = file.readlines()

        first = True

        for i, line in enumerate(data):

            # parte 1
            try:
                #match = re.fullmatch(r"^# Measure \s* (\w+),\s*\w+,.*,\s*(\d+| \d+.\d+)\s*,\s*, \w+$", line)
                match = re.fullmatch(r"^# Measure .+", line)

                # print(match)
                # print(type(match))
                if match:
                    if first:
                        df_dict[match.group(1)] = [match.group(2)]
                    else:
                        df_dict[match.group(1)].append(
                            match.group(2))
            except:
                print("error in part one of stats")

            # parte 2
            try:
                if not line.startswith("#"):
                    values = line.strip().split("\t")
                    if first:
                        df_dict[values[4] + " volume"] = [values[3]]
                    else:
                        df_dict[f"{values[4]} volume"].append(values[3])

                first = False

            except:
                print("error in part two of stats")

        return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    base_path = '/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output_Comparison_AD/'

    # the filename of the stats to extract
    filename = 'aseg.stats'

    subj_paths = extract_path(filename, base_path)
    if subj_paths:
        print("stats file found for " + str(len(subj_paths)) + " subjects")
        stats(subj_paths).to_csv("aseg.csv")
    else:
        print("no file found")
