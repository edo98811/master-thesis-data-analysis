import zipfile
import os
import pandas as pd
import shutil
import csv
import re
import data_manipulation as dm

def extract_path(filename, base_path, subj_list):
    subj_list_numbers = []

    for s in subj_list:
        if len(s.split("/")) > 4:
            subj_list_numbers.append(s.split("/")[-4])
    print(subj_list_numbers)

    subjs_path = []
    for path, subdirs, files in os.walk(base_path):
        if path.split("/")[-1] == 'stats' and path.split("/")[-2] in subj_list_numbers:
            for name in files:
                if name == filename:
                    subjs_path.append(path + "/" + name)

    if not subjs_path:
        return False

    return subjs_path


def stats_aseg(subj_paths):
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
            match = re.match(r"^# Measure (\w+).+(\d+ | \d+\.\d+),\s.+$", line)

            if match:
                # if it's the first iteration it creates the lists, assumes all the files are the same (which should be)
                if not n:
                    df_dict[match.group(1)] = [match.group(2)]
                else:
                    df_dict[match.group(1)].append(
                        match.group(2))

            # part 2
            if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                values = line.strip().split()  # extracts the words and puts them in lists

                if not n:
                    df_dict[values[4] + " volume"] = [values[3]]  # the volume is in column 4(index 3) name in column 5
                else:
                    df_dict[f"{values[4]} volume"].append(values[3])

    #dm.write_dict(df_dict,"prova_df_dict.json")
    return pd.DataFrame.from_dict(df_dict, orient='columns')


def stats_aparcDTK(subj_paths):
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
            match = re.match(r"^# Measure (\w+,\s\w+).+(\d+ | \d+\.\d+),\s.+$", line)

            if match:
                # if it's the first iteration it creates the lists, assumes all the files are the same (which should be)
                if not n:
                    df_dict[match.group(1)] = [match.group(2)]
                else:
                    if match.group(1) not in df_dict.keys():
                        df_dict[match.group(1)] = ["NaN"]
                    else:
                        df_dict[match.group(1)].append(match.group(2))


            # part 2
            if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                values = line.strip().split()  # extracts the words and puts them in lists

                if not n:
                    df_dict[values[0] + " mean thickness"] = [values[2]]  # the volume is in column 4(index 3) name in column 5
                else:
                    df_dict[f"{values[0]} mean thickness"].append(values[2])

        # if some columns have different length
        for key in df_dict.keys():
            if len(df_dict[key]) != n + 1:
                df_dict[key].append("NaN")

    dm.write_dict(df_dict, "prova_df_dict.json")

    # if some columns have different length
    #for key in df_dict.keys():
    #    if len(df_dict[key]) != n+1:
    #        for _ in range(10 - len(df_dict[key])):
    #            df_dict[key].append("NaN")

    return pd.DataFrame.from_dict(df_dict, orient='columns')

def calculate_stats(filename, fileneame_save, base_path, save_path, subj_list, type):

    subj_paths = extract_path(filename, base_path, subj_list)
    if subj_paths:
        print("stats file found for " + str(len(subj_paths)) + " subjects")
        if type == 0:
            stats_aseg(subj_paths).to_csv(save_path + fileneame_save, index=False)
        elif type == 1:
            stats_aparcDTK(subj_paths).to_csv(save_path + fileneame_save, index=False)
    else:
        print("no file found")

if __name__ == "__main__":
    base_path = '/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/'
    save_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/Stats_Freesurfer/"

    healthy = dm.load_txt("paths_healthy_all.txt")
    AD = dm.load_txt("paths_AD_dementia_all.txt")

    calculate_stats('aseg.stats', "aseg_healthy.csv", base_path, save_path, healthy, 0)
    calculate_stats('aseg.stats', "aseg_AD.csv", base_path, save_path, AD, 0)
    calculate_stats('rh.aparc.DKTatlas.stats', "aparcDKT_left_AD.csv.csv", base_path, save_path, AD, 1)
    calculate_stats('rh.aparc.DKTatlas.stats', "aparcDKT_left_healthy.csv.csv", base_path, save_path, healthy, 1)
    calculate_stats('lh.aparc.DKTatlas.stats', "aparcDKT_right_AD.csv.csv", base_path, save_path, healthy, 1)
    calculate_stats('lh.aparc.DKTatlas.stats', "aparcDKT_right_healthy.csv.csv", base_path, save_path, AD, 1)
    #
    # # aseg
    # filename = 'aseg.stats'
    #
    # subj_paths = extract_path(filename, base_path, healthy)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aseg(subj_paths).to_csv(save_path + "aseg_healthy.csv", index=False)
    # else:
    #     print("no file found")
    #
    # filename = 'aseg.stats'
    #
    # subj_paths = extract_path(filename, base_path, AD)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aseg(subj_paths).to_csv(save_path + "aseg_AD.csv", index=False)
    # else:
    #     print("no file found")
    #
    # # AD
    # # left hemisphere
    # # the filename of the stats to extract
    # filename = 'lh.aparc.DKTatlas.stats'
    #
    # subj_paths = extract_path(filename, base_path, AD)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aparcDTK(subj_paths).to_csv(save_path + "aparcDKT_left_AD.csv", index=False)
    # else:
    #     print("no file found")
    #
    # # right hemisphere
    # filename = 'rh.aparc.DKTatlas.stats'
    #
    # subj_paths = extract_path(filename, base_path, AD)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aparcDTK(subj_paths).to_csv(save_path + "aparcDKT_right_AD.csv", index=False)
    # else:
    #     print("no file found")
    #
    #
    # # healthy
    # # left hemisphere
    # filename = 'lh.aparc.DKTatlas.stats'
    #
    # subj_paths = extract_path(filename, base_path, healthy)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aparcDTK(subj_paths).to_csv(save_path + "aparcDKT_left_healthy.csv", index=False)
    # else:
    #     print("no file found")
    #
    # # right hemisphere
    # filename = 'rh.aparc.DKTatlas.stats'
    #
    # subj_paths = extract_path(filename, base_path, healthy)
    # if subj_paths:
    #     print("stats file found for " + str(len(subj_paths)) + " subjects")
    #     stats_aparcDTK(subj_paths).to_csv(save_path + "aparcDKT_right_healthy.csv", index=False)
    # else:
    #     print("no file found")