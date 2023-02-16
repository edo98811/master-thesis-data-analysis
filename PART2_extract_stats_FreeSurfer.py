import zipfile
import os
import pandas as pd
import shutil
import csv
import re
import data_manipulation as dm

BASE_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
SAVE_PATH = '/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/Stats_FreeSurfer/'
TABLE_PATH = '/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/text_and_csv_files/OASIS_table.csv'


def main():
    table = pd.read_csv(TABLE_PATH)
    subjects_list = table.query("processed=='yes'")["ID"].tolist()

    for i, subj in enumerate(subjects_list):
        subjects_list[i] = "sub-" + subj

    # note: 0-> aseg, 1-> apark
    calculate_stats('aseg.stats', "aseg.csv", subjects_list, 0)
    calculate_stats('lh.aparc.DKTatlas.stats', "aparcDKT_left.csv", subjects_list, 1)
    calculate_stats('rh.aparc.DKTatlas.stats', "aparcDKT_right.csv", subjects_list, 1)


"""
DESCRIPTION 

    
"""


def calculate_stats(stats_filename, save_filename, subj_list, _type):
    stat_file_paths = extract_path(stats_filename, subj_list)

    if stat_file_paths:
        print("stats file found for " + str(len(stat_file_paths)) + " subjects")
        if _type == 0:
            stats_aseg(stat_file_paths).to_csv(SAVE_PATH + save_filename, index=False)
        elif _type == 1:
            stats_aparcDTK(stat_file_paths).to_csv(SAVE_PATH + save_filename, index=False)
    else:
        print("no file found")


def extract_path(filename, subj_list):
    # set of all the subjects for easier computation
    subj_list_numbers = set(subj_list)

    # creates a list with all the subjects that are in the list
    # for s in subj_list:
    #     if len(s.split("/")) > 4:
    #         subj_list_numbers.add(s.split("/")[-4])
    # print(subj_list_numbers)

    paths_found = []
    for path, subdirs, files in os.walk(BASE_PATH):
        if path.split("/")[-1] == 'stats' and path.split("/")[-2] in subj_list_numbers:
            for name in files:
                if name == filename:
                    paths_found.append(path + "/" + name)

    if not paths_found:
        return False

    return paths_found


def stats_aseg(subj_paths):
    df_dict = {"ID": []}

    for n, path in enumerate(subj_paths):
        print("extracting stats for subject " + str(n + 1) + ", path:" + path)

        # saving the subject name
        df_dict["ID"].append(path.split("/")[-3])

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
                    if match.group(1) in df_dict.keys():
                        df_dict[match.group(1)].append(match.group(2))
                    else:
                        df_dict[match.group(1)] = ["NaN" for _ in range(n)]  # if there are NaN
                        df_dict[match.group(1)].append(match.group(2))
            # part 2
            if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                values = line.strip().split()  # extracts the words and puts them in lists

                if not n:
                    df_dict[values[4] + "_volume_mm3"] = [
                        values[3]]  # the volume_mm3 is in column 4(index 3) name in column 5
                else:
                    if f"{values[4]}_volume_mm3" in df_dict.keys():
                        df_dict[f"{values[4]}_volume_mm3"].append(values[3])
                    else:
                        df_dict[values[4] + "_volume_mm3"] = ["NaN" for _ in range(n)]
                        df_dict[f"{values[4]}_volume_mm3"].append(values[3])

        # if some columns have different length at the end pf a cycle
        for key in df_dict.keys():
            if len(df_dict[key]) != n + 1:
                df_dict[key].append("NaN")

    # # if some columns have different length
    # for key in df_dict.keys():
    #    if len(df_dict[key]) != n+1:
    #        for _ in range(n+1 - len(df_dict[key])):
    #            df_dict[key].append("NaN")

    # dm.write_dict(df_dict,"prova_df_dict.json")
    return pd.DataFrame.from_dict(df_dict, orient='columns')


def stats_aparcDTK(subj_paths):
    df_dict = {"ID": []}

    for n, path in enumerate(subj_paths):
        print("extracting stats for subject " + str(n + 1) + ", path:" + path)

        # saving the subject name
        df_dict["ID"].append(path.split("/")[-3])

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
                    df_dict[match.group(1).replace(" ", "")] = [match.group(2)]
                else:
                    if match.group(1).replace(" ", "") in df_dict.keys():
                        df_dict[match.group(1).replace(" ", "")].append(match.group(2))
                    else:
                        df_dict[match.group(1).replace(" ", "")] = ["NaN" for _ in range(n)]
                        df_dict[match.group(1).replace(" ", "")].append(match.group(2))

            # part 2
            if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                values = line.strip().split()  # extracts the words and puts them in lists

                if not n:
                    df_dict[values[0] + "_mean_thickness_mm"] = [
                        values[4]]  # the thickness is in column 4(index 3) name in column 5
                else:
                    if f"{values[0]}_mean_thickness_mm" in df_dict.keys():
                        df_dict[f"{values[0]}_mean_thickness_mm"].append(values[4])
                    else:
                        df_dict[values[0] + "_mean_thickness_mm"] = ["NaN" for _ in range(n)]
                        df_dict[values[0] + "_mean_thickness_mm"].append(values[4])

                if not n:
                    df_dict[values[0] + "_mean_area_mm2"] = [
                        values[2]]  # the area is in column 3(index 2) name in column 5
                else:
                    if f"{values[0]}_mean_area_mm2" in df_dict.keys():
                        df_dict[f"{values[0]}_mean_area_mm2"].append(values[2])
                    else:
                        df_dict[values[0] + "_mean_area_mm2"] = ["NaN" for _ in range(n)]
                        df_dict[values[0] + "_mean_area_mm2"].append(values[2])

        # if some columns have different length at the end of a cycle
        for key in df_dict.keys():
            if len(df_dict[key]) != n + 1:
                df_dict[key].append("NaN")

    dm.write_dict(df_dict, "old scripts/prova_df_dict.json")

    # # if some columns have different length
    # for key in df_dict.keys():
    #    if len(df_dict[key]) != n+1:
    #        for _ in range(n + 1 - len(df_dict[key])):
    #            df_dict[key].append("NaN")

    return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    main()
