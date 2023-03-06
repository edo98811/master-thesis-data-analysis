import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from scipy import stats
import seaborn as sns
import data_manipulation as dm
import numpy as np
# import dropboxAPI
import subprocess

# todo altro:
"""

- rileggere tutto 
- metodo per avviare codice fastsurfer


cose da chiedere 
- script per ogni area (quali sono le aree più importanti) 
- quali soggetti dovrei tenere per fastsurfer (che patologie) 

todo
    - bonferroni correction da sempre problemi 
    - mettere a posto i nomi dei grafici salvati
    - aggiungere modo di salvare parametri anche in stats free (adesso si puo fare solo per stats fast)
    - in Stats il processed path deve essere preso direttamente dalle Table, forse anche il processed path?
    - in comparison serve davvero il parametro column to test?
    - fare il metodo per caricare l'età dei soggetti 
    - aggiungere print alla fine delle funzioni
    - aggiungere descrizioni fatte bene
    - riscrivere tutto usando inheritance
    - quando faccio la selezione delle colonne aggiungere un testo che mi dice cosa sto escludendo (quali colonne)
    - salvare in log i dati che non vanno (ad esempio nello stat test) quando dice che absent or invalid data in un file di testo 
        tipo log 
    - aggiungere metodo per controllare che le figure siano salvate correttamente (e tutte)

idee
    - input nella funzione table anche la struttura delle tabelle per creare la tabella nuova (magari richiamata) 

"""


class Table:
    """
    init:
        df =
        processed_path =
        subjects_list =
        base_path =

    attributes

    methods

        get_query(self, query):

        update(self):

        get_query(self, query, sub=False, only_processed=True):

        save_csv(self, filename):

    """

    def __init__(self, name, b_path, p_path, df_subj=None, d_folder="data_testing/"):
        """
        :param name: str - name of the object
        :param b_path: str - base path
        :param p_path: str - path to check for processed images
        :param df_subj: pd.df the dataframe of subjects
        :param d_folder: str - data folder (default: data_testing/)
        """
        if df_subj is not None:
            self.df = df_subj
        else:
            self.create_table()
        self.subjects_list = self.df["ID"].tolist()

        self.processed_path = p_path
        self.base_path = b_path
        self.data_path = d_folder
        self.name = name

    # def get_query_list(self, query):
    #     """
    #     old
    #
    #     :param query:
    #     :return:
    #     """
    #     subjects_list = self.df.query(query)["ID"].tolist()
    #     for i, s in enumerate(subjects_list):
    #         subjects_list[i] = "sub-" + s
    #
    #     self.subjects_list = set(subjects_list)
    def update(self):
        """
        function to update the table
        :return:
        """
        # for i, subj_path_filtered in enumerate(df["ID"].tolist()):
        #     subjs.add("sub-" + subj_path_filtered)

        # iterate though all the directories in the processed path
        for root, dirs, files in os.walk(self.processed_path):
            for dir in dirs:
                if dir in self.subjects_lists:
                    # quando trova il soggetto nella cartella modifica il dataframe
                    for i, subj_path_filtered in enumerate(self.df["ID"].tolist()):
                        if dir == "sub-" + subj_path_filtered:
                            self.df.loc[i, "processed"] = "yes"
                            self.df.loc[i, "processed_path"] = root + "/" + dir
                            break

    def create_table(self, df_dict_map, path_to_origin_file):
        """
        method to create the table if it doesn't exist
        :return:
        """
        raise "method not yet implemented"

        table = pd.read_csv(self.base_path + path_to_origin_file)

        # create the dictionary that will turn into a table
        if ADNI:
            df_dict = {
                "ID": [],
                "path": [],
                "age": [],
                "sex": [],
                "main_condition": [],
                "processed": [],
                "processed_path": []
            }
        else:
            df_dict = {
                "ID": [],
                "path": [],
                "age": [],
                "main_condition": [],
                "processed": [],
                "processed_path": []
            }

        # populates the dictionary
        for index, row in table.iterrows():
            for i, path_on_table in enumerate(_paths_on_table):
                if len(path_on_table.split("/")) > 3:
                    match = re.split("sub-", path_on_table.split("/")[-4])
                    if row["ID"] == match[1]:
                        if ADNI and (row["_merge"] == "both" or row["_merge"] == "right_only"):
                            df_dict["ID"].append(row["ID"])
                            df_dict["path"].append(path_on_table)
                            df_dict["age"].append(row["age"])
                            df_dict["sex"].append(row["sex"])
                            df_dict["main_condition"].append(row["diagnosis"])
                            df_dict["processed"].append("no")
                            df_dict["processed_path"].append("")
                        elif not ADNI:
                            df_dict["ID"].append(row["ID"])
                            df_dict["path"].append(path_on_table)
                            df_dict["age"].append(row["ageAtEntry"])
                            df_dict["main_condition"].append(row["dx1"])
                            df_dict["processed"].append("no")
                            df_dict["processed_path"].append("")

        df = pd.DataFrame.from_dict(df_dict)

        subjs = set()

        # adds the paths
        # interate though all the rows to create a set of the subjects
        for i, subj_path_filtered in enumerate(df["ID"].tolist()):
            df.loc[i, "processed"] = "no"
            subjs.add("sub-" + subj_path_filtered)

        # iterate though all the directories in the processed path
        for root, dirs, files in os.walk(PROCESSED_PATH):
            for dir in dirs:
                if dir in subjs:
                    # quando trova il soggetto nella crtela modifica il dataframe
                    for i, subj_path_filtered in enumerate(df["ID"].tolist()):
                        if dir == "sub-" + subj_path_filtered:
                            df.loc[i, "processed"] = "yes"
                            df.loc[i, "processed_path"] = root + "/" + dir
                            break

        return df

    def get_query(self, query, sub=False, only_processed=True):
        """
        function to filter the data in the table
        :param query: str - pandas query to apply to the df
        :param sub: bool - return the list of subjects or the list of folders which have sub- in front (default = False)
        :param only_processed: bool - returns only the subjects that respect the query and have been processed already (default = True)
        :return: pd.df - filtered
        """
        # print (self.df.head())
        """
        :param query:
        :param sub:
        :param only_processed:
        :return: df or list
        """
        if sub:
            if only_processed:
                df = self.df.query("processed==yes")
            else:
                df = self.df

            subjects_list = df.query(query)["ID"].tolist()
            for i, s in enumerate(subjects_list):
                subjects_list[i] = "sub-" + s

            return subjects_list

        # df = self.df.loc[df_subj.loc['ID'].isin(subjects_list)]

        df = self.df.query(query)
        if only_processed:
            df = df.loc[df['processed'] == 'yes']
        print(f"table: {self.name} filtered throug query: {query}, {len(df)} subjects found")
        return df

    def save_csv(self, filename):

        """
        saves the df to csv in basepath + filename
        :param filename: str - the filename that the csv file will have once saved
        :return: void
        """
        self.df.to_csv(self.data_path + filename)
        print(f"csv of table {self.name} saved in {self.data_path + filename}")

    def start_processing(self):
        """
        to be implemented - starts the fastsurfer processing
        :return:
        """
        pass
        # subprocess.

    """
    def add_sub(self, subjects_list):
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s
        return subjects_list
    """


class Stats:
    """
    init
        df subj
        name
        base path

        query (necessary se non vengono dati

        aparcLeft
        aparcRight
        aseg

    attributes

    methods
    """

    def __init__(self, name, b_path, df_subj_obj, query, d_folder="data_testing/",
                 p_path="/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output", aseg=None,
                 aparcLeft=None, aparcRight=None):
        """
        :param name: str - name of the object
        :param b_path: str - base path
        :param df_subj_obj: Table -
        :param query: if data need to be filtered
        :param d_folder: str - data folder (default: data_testing/)
        :param p_path: str - the path in which to look for the processing  (default: "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output")
        :param aseg: pd.df
        :param aparcLeft: pd.df
        :param aparcRight: pd.df
        """
        # here it is saved the data object of the dataset
        if isinstance(df_subj_obj, Table):
            self.df_subj_obj = df_subj_obj
        else:
            raise "wrong datatype"

        # here there is the df only already filtered
        self.df_subj = df_subj_obj.get_query(query)
        self.subj_list = self.add_sub(self.df_subj["ID"].tolist())

        self.processed_path = p_path
        self.base_path = b_path
        self.data_path = self.base_path + d_folder

        # if not query or (not aseg or not aparcLeft or not aparcRight):
        #     raise " non va bene"

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.query = query
        self.name = name

        # add control that these data are dataframes
        if aparcLeft is not None:
            self.df_stats_aparcL = aparcLeft
            self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(self.subj_list)]
        else:
            self.df_stats_aparcL = self.extract_stats_fast('rh.aparc.DKTatlas.mapped.stats', 1)
            self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(self.subj_list)]
        if aparcRight is not None:
            self.df_stats_aparcR = aparcRight
            self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR[ "ID"].isin(self.subj_list)]
        else:
            self.df_stats_aparcR = self.extract_stats_fast('lh.aparc.DKTatlas.mapped.stats', 1)
            self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR[ "ID"].isin(self.subj_list)]
        if aseg is not None:
            self.df_stats_aseg = aseg
            self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg[ "ID"].isin(self.subj_list)]
        else:
            self.df_stats_aseg = self.extract_stats_fast('aseg.stats', 0)
            self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg[ "ID"].isin(self.subj_list)]

    def add_sub(self, list):
        """
        :param list: list of str - list of subj names
        :return:
        """
        for i, s in enumerate(list):
            list[i] = "sub-" + s
        return list

    def extract_stats_fast(self, stats_filename, _type):
        """
        :param stats_filename: str
        :param _type: int aseg or aparc (0 or 1)
        :return:
        """
        stat_df_paths = self.__extract_path(stats_filename)

        if stat_df_paths:
            print(f"stats file {stats_filename} found for {str(len(stat_df_paths))} subjects")
            if _type == 0:
                # __(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__fast_stats_aseg(stat_df_paths)
            elif _type == 1:
                # stats_aparcDTK(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__fast_stats_aparcDTK(stat_df_paths)
        else:
            print(f"no stat file: {stats_filename} file found in {self.processed_path}")

    def extract_stats_free(self, stats_filename, _type):
        """
        :param stats_filename: str
        :param _type: int aseg or aparc (0 or 1)
        :return:
        """
        stat_df_paths = self.__extract_path(stats_filename)

        if stat_df_paths:
            print("stats file found for " + str(len(stat_df_paths)) + " subjects")
            if _type == 0:
                # __(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__free_stats_aseg(stat_df_paths)
            elif _type == 1:
                # stats_aparcDTK(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__free_stats_aparcDTK(stat_df_paths)
        else:
            print("no file found")

    def save_stats_files(self, which=(True, True, True), names=("aseg.csv", "aseg_right.csv", "aseg_left.csv")):
        """
        :param which: tuple of bool - which files to save (default: True, True, True)
        :param names: tuple - names of the files (default: "aseg.csv", "aseg_right.csv", "aseg_left.csv")
        :return:
        """

        if not os.path.exists(self.data_path + self.name):
            os.makedirs(self.data_path + self.name)

        if which[0]:
            self.df_stats_aseg.to_csv(self.data_path + self.name + "/" + names[0])
        if which[1]:
            self.df_stats_aparcL.to_csv(self.data_path + self.name + "/" + names[1])
        if which[2]:
            self.df_stats_aparcR.to_csv(self.data_path + self.name + "/" + names[2])

    def __fast_stats_aseg(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # print("extracting stats for subject " + str(n + 1) + ", path:" + path)

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

    def __fast_stats_aparcDTK(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # print("extracting stats for subject " + str(n + 1) + ", path:" + path)

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

        # dm.write_dict(df_dict, "old scripts/prova_df_dict.json")

        # # if some columns have different length
        # for key in df_dict.keys():
        #    if len(df_dict[key]) != n+1:
        #        for _ in range(n + 1 - len(df_dict[key])):
        #            df_dict[key].append("NaN")

        return pd.DataFrame.from_dict(df_dict, orient='columns')

    def __free_stats_aseg(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # print("extracting stats for subject " + str(n + 1) + ", path:" + path)

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

    def __free_stats_aparcDTK(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # print("extracting stats for subject " + str(n + 1) + ", path:" + path)

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

        # dm.write_dict(df_dict, "old scripts/prova_df_dict.json")

        # # if some columns have different length
        # for key in df_dict.keys():
        #    if len(df_dict[key]) != n+1:
        #        for _ in range(n + 1 - len(df_dict[key])):
        #            df_dict[key].append("NaN")

        return pd.DataFrame.from_dict(df_dict, orient='columns')

    def __extract_path(self, filename):
        # set of all the subjects for easier computation
        subj_list_numbers = set(self.subj_list)

        # creates a list with all the subjects that are in the list
        # for s in subj_list:
        #     if len(s.split("/")) > 4:
        #         subj_list_numbers.add(s.split("/")[-4])
        # print(subj_list_numbers)
        # to be updated for every processed paths

        paths_found = []
        for path, subdirs, files in os.walk(self.processed_path):
            if path.split("/")[-1] == 'stats' and path.split("/")[-2] in subj_list_numbers:
                for name in files:
                    if name == filename:
                        paths_found.append(path + "/" + name)

        if not paths_found:
            return False

        return paths_found


class Comparisons:
    """
    init args

    attributes
        df1
        df2

        name
        alpha
        maxplots

        column list
        subj list

        stat result

    methods
        bonferroni correction

        stat test

        violin plot

        bland altmann plot
    """

    def __init__(self, name, b_path, stats_df_1, stats_df_2, alpha=0.05, d_folder="data_testing/", columns_to_test=None,
                 max_plot=500):
        """
        :param name: str - name of the object
        :param b_path: str - base path
        :param stats_df_1: Stats -
        :param stats_df_2: Stats -
        :param alpha: float - significance treshold of stat test (default: 0.05)
        :param d_folder: str - data folder (default: data_testing/)
        :param columns_to_test:
        :param max_plot:
        """
        if isinstance(stats_df_1, Stats):
            self.stat_df_1 = stats_df_1
        else:
            raise "stats of the wrong class"
        if isinstance(stats_df_2, Stats):
            self.stat_df_2 = stats_df_2
        else:
            raise "stats of the wrong class"
        self.base_path = b_path

        self.data_path = self.base_path + d_folder
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # aggiungere controllo che i soggetti siano gli stessi e non diversi
        # tmp = self.stat_df_1.df_subj["ID"].tolist()
        # self.subjects_list = {tmp.extend(self.stat_df_2.df_subj["ID"].tolist())}
        # tmp = self.stat_df_1.df_subj.columns.tolist()
        # self.columns_list = {tmp.extend(self.stat_df_2.df_subj.columns.tolist())}
        # del tmp

        self.subjects_list = set(self.stat_df_1.df_subj["ID"].tolist()).intersection(
            set(self.stat_df_2.df_subj["ID"].tolist()))
        self.columns_list = set(self.stat_df_1.df_subj.columns.tolist()).intersection(
            set(self.stat_df_2.df_subj.columns.tolist()))

        if not self.subjects_list or not self.columns_list:
            raise "datasets dont have elements in common"
        if not os.path.exists(self.data_path + "images/"):
            os.makedirs(self.data_path + "images/")

        self.name = name
        self.alpha = alpha
        self.updated_alpha = "no correction"
        self.max_plot = max_plot

        self.stat_df_result = None
        self.stat_test(columns_to_test)

    def violin(self, data="aseg", columns=None, n_subplots=10, n_rows=2):
        """
        :param data: str - table to select (aseg, aparcL, aparcR)
        :param columns: list  of str- list of column names to print (default None: prints all)
        :param n_subplots: int - n of subplots in image (default 4)
        :param n_rows: int - n of rows in plot (default 2)
        :return: void
        """
        plots = 0

        if data == "aseg":
            _df1 = self.stat_df_1.df_stats_aseg
            _df2 = self.stat_df_2.df_stats_aseg
        elif data == "aparcR":
            _df1 = self.stat_df_1.df_stats_aparcL
            _df2 = self.stat_df_2.df_stats_aparcL
        elif data == "aparcL":
            _df1 = self.stat_df_1.df_stats_aparcR
            _df2 = self.stat_df_2.df_stats_aparcR
        else:
            raise "violin: wrong selection parameter"

        # if not columns:
        #     columns = _df1.columns
        #     columns = columns.intersection(_df2.columns).tolist()
        # select the columns that exist in both the datasets
        if not columns:
            columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))
        # if not columns:
        #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     columns = range(2, max_len)

        for column_to_compare in columns:
            a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
            b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')
            # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):

                if not plots % n_subplots:
                    if plots > 1:
                        fig.savefig(
                            self.data_path + "images/img_violin_" + self.name + "_" + str(
                                plots) + ".png")  # save the figure to file
                        # plt.close(fig)  # close the figure window
                        # handles, labels = axs[1].get_legend_handles_labels()
                        # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})F
                    fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
                    axs = axs.ravel()
                    plt.subplots_adjust(hspace=0.5)
                    plt.subplots_adjust(wspace=0.2)
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                index = plots % n_subplots
                #print(index)
                self.__violin_plot(axs[index], a, b)
                plots += 1

            if plots >= self.max_plot:  # to avoid plotting too much
                break

        fig.savefig(
            self.data_path + "images/img_scatter_" + self.name + " - " + self.name + "_" + str(
                plots) + ".png")  # save the figure to file
    def bland_altmann(self, data="aseg", columns=None, n_subplots=4, n_rows=2):
        """
        :param data: str - table to select (aseg, aparcL, aparcR)
        :param columns: list  of str- list of column names to print (default None: prints all)
        :param n_subplots: int - n of subplots in image (default 4)
        :param n_rows: int - n of rows in plot (default 2)
        :return: void
        """
        plots = 0

        if data == "aseg":
            _df1 = self.stat_df_1.df_stats_aseg
            _df2 = self.stat_df_2.df_stats_aseg
        elif data == "aparcR":
            _df1 = self.stat_df_1.df_stats_aparcL
            _df2 = self.stat_df_2.df_stats_aparcL
        elif data == "aparcL":
            _df1 = self.stat_df_1.df_stats_aparcR
            _df2 = self.stat_df_2.df_stats_aparcR

        if not columns:
            columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))  # set with columns
            # columns = _df1.columns
            # columns = columns.intersection(_df2.columns).tolist()
        # if not columns:
        #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     columns = range(2, max_len)

        for column_to_compare in columns:
            a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
            b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')
            # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):  # for all the fields with numbers

                if not plots % n_subplots:
                    if plots > 1:
                        fig.savefig(
                            self.data_path + "images/img_ba_" + self.name + "_" + str(
                                plots) + ".png")  # save the figure to file
                        # handles, labels = ax.get_legend_handles_labels()
                        # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
                    fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
                    axs = axs.ravel()
                    plt.subplots_adjust(hspace=0.5)
                    plt.subplots_adjust(wspace=0.2)
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                index = plots % n_subplots
                #print(index)
                self.__bland_altman_plot(axs[index], a, b)
                plots += 1

            if plots >= 20:  # to avoid plotting too much
                break

        fig.savefig(
            self.data_path + "images/img_scatter_" + self.name + " - " + self.name + "_" + str(
                plots) + ".png")  # save the figure to file
    def stat_test(self, columns, data="aseg"):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :return: void
        """
        if data == "aseg":
            _df1 = self.stat_df_1.df_stats_aseg
            _df2 = self.stat_df_2.df_stats_aseg
        elif data == "aparcR":
            _df1 = self.stat_df_1.df_stats_aparcL
            _df2 = self.stat_df_2.df_stats_aparcL
        elif data == "aparcL":
            _df1 = self.stat_df_1.df_stats_aparcR
            _df2 = self.stat_df_2.df_stats_aparcR
        else:
            raise "stat_test: wrong selection parameter"

        r_all = []
        print(f"performing t_test and mann whitney on {data} in {self.name}")

        # se non viene dato un input fa il test per tutte le colonne
        if not columns:
            columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))
        # if not columns:
        #     columns = _df1.columns
        #     columns.intersection(_df2_filtered.columns).tolist()
        # if not columns:
        #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     columns = range(2, max_len)

        for column_to_compare in columns:
            a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
            b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')
            # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                print(f"performing statistical analysis for data in category {column_to_compare}for file {self.name} - {data}")

                r1, p1, o1 = self.__mann_whitney(a, b)
                r2, p2, o2 = self.__t_test(a, b)
                d, rd = self.__cohens_d(a, b)  # between two areas

                if isinstance(column_to_compare, int):
                    column_to_compare_name = _df1.columns[column_to_compare]

                    r_all.append({"name": f"{self.name} {column_to_compare_name}",
                                  "mann_whitney": {"result": r1,
                                                   "p_value": p1,
                                                   "outcome": o1},
                                  "t_test": {"result": r2,
                                             "p_value": p2,
                                             "outcome": o2},
                                  "d": {"result": rd,
                                        "d_value": d}})

                if isinstance(column_to_compare, str):
                    r_all.append({"name": f"{self.name} {column_to_compare}",
                                  "mann_whitney": {"result": r1,
                                                   "p_value": p1,
                                                   "outcome": o1},
                                  "t_test": {"result": r2,
                                             "p_value": p2,
                                             "outcome": o2},
                                  "d": {"result": rd,
                                        "d_value": d}})

            else:
                print(f"absent or not valid data in category {column_to_compare}for file {self.name} - {data}")
            self.__save_dataframe(r_all)

    def bonferroni_correction(self, save=False):
        """
        :param save: bool - if true save the file after correction
        :return: void
        """
        # print(self.updated_alpha)
        self.updated_alpha = self.__correction_param()
        # print(self.updated_alpha)
        for i, row in self.stat_df_result.iterrows():
            if type(row["mann_whitney p_value"]) is not str and type(row["mann_whitney p_value"]) is not str and type(
                    self.updated_alpha) is not str:
                if row["mann_whitney p_value"] < self.updated_alpha:
                    row[
                        "mann_whitney message"] = f"p-value: {row['mann_whitney p_value']} - null hypothesis rejected, means are not statistically equal"
                    row["mann_whitney outcome"] = 1
            if type(row["t_test p_value"]) is not str and type(row["t_test p_value"]) is not str and type(
                    self.updated_alpha) is not str:
                if row["t_test p_value"] < self.updated_alpha:
                    row[
                        "t_test message"] = f"p-value: {row['t_test p_value']} - null hypothesis rejected, the datasets have a different distribution"
                    row["t_test outcome"] = 1
            row.loc["alpha_correction"] = self.updated_alpha
            self.stat_df_result.loc[i, :] = row
            if save:
                self.stat_df_result.to_csv(self.data_path + f"{self.name}_bonferroni_corrected.csv")

    def save_data(self, filename):
        """
        to csv in basepath + filename
        :param filename: str - name of the file to be saved into
        :return:
        """
        self.stat_df_result.to_csv(self.data_path + filename)

    def __t_test(self, _a, _b):
        # a, b = get_column(column_to_compare, df1, df2)

        if "NaN" in _a or "NaN" in _b:
            print("could not compute")
            return "result could not be computed", "NaN", "NaN"

        t_stat, p_value = stats.ttest_ind(_a, _b)

        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"
            outcome = 1

        return result, p_value, outcome

    def __mann_whitney(self, _a, _b):
        # a, b = get_column(column_to_compare, df1, df2)

        if "NaN" in _a or "NaN" in _b:
            return "result could not be computed", "NaN", "NaN"

        # df1.to_csv("dataset_uniti_test.csv", index=False)

        t_stat, p_value = stats.mannwhitneyu(_a, _b)

        # p value is the likelihood that these are the same
        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"
            outcome = 1

        return result, p_value, outcome

    def __save_dataframe(self, list_to_save):
        self.stat_df_result = pd.DataFrame()

        for item in list_to_save:
            self.stat_df_result = pd.concat(
                [self.stat_df_result, pd.DataFrame({"mann_whitney p_value": item["mann_whitney"]["p_value"],
                                                    "mann_whitney outcome": item["mann_whitney"]["outcome"],
                                                    "mann_whitney message": item["mann_whitney"]["result"],
                                                    "t_test p_value": item["t_test"]["p_value"],
                                                    "t_test outcome": item["t_test"]["outcome"],
                                                    "t_test message": item["t_test"]["result"],
                                                    "cohens d value": item["d"]["d_value"],
                                                    "cohens d result": item["d"]["result"],
                                                    "alpha_used": self.alpha,
                                                    "alpha_correction": self.updated_alpha
                                                    }, index=[item["name"]])])

        # df.to_csv(self.base_path + _name)  # , index=False

    def __cohens_d(self, _a, _b):
        n1, n2 = len(_a), len(_b)
        var1, var2 = np.var(_a, ddof=1), np.var(_b, ddof=1)

        SDpooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        d = (np.mean(_a) - np.mean(_b)) / SDpooled

        if d < 0.2:
            string = "Very small effect size"
        elif d < 0.5:
            string = "Small effect size"
        elif d < 0.8:
            string = "Medium effect size"
        else:
            string = "Large effect size"

        return d, string

    def __violin_plot(self, _ax, _a, _b):
        # Create a DataFrame with the two Series
        # df = pd.DataFrame({'Freesurfer': _a, 'Fastsurfer': _b})
        df = pd.DataFrame({'Data': pd.concat([_a, _b]),
                           'Group': ['FreeSurfer'] * len(_a) + ['FastSurfer'] * len(_b),
                           "Area": [_a.name] * (len(_a) + len(_b))})

        # Create a split violin plot
        # sns.violinplot(data=df, split=True)
        sns.violinplot(ax=_ax, data=df, hue="Group", x="Area", y="Data", split=True)
        _ax.title.set_text(_a.name + "\n" + self.name)
        # ax.yaxis.set_major_formatter(plt.FormatStrFormatter('{:.3g}'))
        _ax.set_xlabel("")

    def __bland_altman_plot(self, _ax, _a, _b):
        # Compute mean and difference between two series
        mean_list = []
        for i, (a,b) in enumerate(zip(_a, _b)):
            mean_list.append((a + b)/2)
        # mean = np.mean([_a,_b], axis=0)ù
        mean = np.array(mean_list)
        diff = _a - _b

        # Compute mean difference and standard deviation of difference
        md = np.mean(diff)
        sd = np.std(diff, axis=0)

        # Create plot
        _ax.scatter(mean, diff, s=10)
        _ax.axhline(md, color='gray', linestyle='--')
        _ax.axhline(md + 1.96 * sd, color='gray', linestyle='--')
        _ax.axhline(md - 1.96 * sd, color='gray', linestyle='--')
        _ax.set_xlabel('Mean')
        _ax.set_ylabel('Difference')
        _ax.set_title(_a.name + "\n" + self.name)  # query.split("=")[-1])
        _ax.legend(['Mean difference', '95% limits of agreement'])
    # def __get_column(self, column_to_compare):
    #     if isinstance(column_to_compare, int):
    #         a = df1.iloc[:, column_to_compare]
    #         b = df2.iloc[:, column_to_compare]
    #
    #     if isinstance(column_to_compare, str):
    #         a = df1.loc[:, column_to_compare]
    #         b = df2.loc[:, column_to_compare]
    #
    #     return a, b
    def __correction_param(self):
        return self.alpha / len(self.stat_df_result)


class SummaryPlot:
    def __init__(self, name, b_path, stats_df_list, d_folder="data_testing/", max_plot=500):
        """

        :param name:
        :param b_path:
        :param df_list: type:stats
        :param d_folder:
        :param max_plot:
        """
        """
        idea: fare una lina per persone sane, una linea per persone malate, una linea per freesurfer e per fastsurfer
        domande da fare:
            per tutte le aree o solo alcune interessanti?
            quali devo confrontare come soggetti?
        """
        self.df_list_obj = stats_df_list

        # else:
        #     raise ("stats of the wrong class")
        self.base_path = b_path
        self.data_path = self.base_path + d_folder

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # self.subjects_list = self.df["ID"].tolist()
        # self.columns_list = self.df.columns.tolist()
        # todo: aggiugere lista soggetti

        self.name = name
        self.max_plot = max_plot

    # in teoria dovrei filtrarla prima
    def comparison_plot(self, data="aseg", columns=None, n_subplots=4, n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        plots = 0

        df_list = []
        # saves the dataframes from the stats object
        if data == "aseg":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aseg)
        elif data == "aparcR":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aparcL)
        elif data == "aparcL":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aparcR) # table

        # creates the age series, to move up
        ages = []
        for table in self.df_list_obj:
            ages.append(table.df_subj.loc[:, "age"].tolist())

        if not columns:
            columns = df_list[0].columns
        # columns = columns.intersection(_df2.columns).tolist()
        # if not columns:
        #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     columns = range(2, max_len)

        for column_to_compare in columns:
            serieses = []
            # selects the column from all the dataframes and puts them in a list of series
            for i, df in enumerate(df_list):
                series = pd.to_numeric(df[column_to_compare], errors='coerce')
                series.rename = f"{data} {self.df_list_obj[i].name} - {column_to_compare}"
                if series.any() and series.notnull().all():
                    serieses.append(series)
                else:
                    # print(series)
                    print(f"scatter not possible for column {column_to_compare}")
                    break
            if not len(serieses):
                continue

            # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            # if it needs to create a new figure it creates it
            if not plots % n_subplots:
                if plots > 1:
                    fig.savefig(
                        self.data_path + "images/img_scatter_" + self.name + " - " + self.name + "_" + str(
                            plots) + ".png")  # save the figure to file
                    # plt.close(fig)  # close the figure window
                    # handles, labels = axs[1].get_legend_handles_labels()
                    # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
                fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
                axs = axs.ravel()
                plt.subplots_adjust(hspace=0.5)
                plt.subplots_adjust(wspace=0.2)
                # mng = plt.get_current_fig_manager()
                # mng.full_screen_toggle()

            # print(plots % N_SUBPLOTS)

            """
            now i have two series
            serieses: series of data
            ages: series of ages 
            
            i can do the scatter plots of this
            """
            print(f"ages {len(ages)} {len(ages[0])}  - {type(ages[0])} {ages[0]}")
            print(f"ages {len(serieses)} {len(serieses[0])} - {type(serieses[0])} {serieses[0]}")
            index = plots % n_subplots
            #print(index)
            self.__scatter_plot(axs[index], serieses, ages)
            plots += 1

            if plots >= self.max_plot:  # to avoid plotting too much
                break

        # fig.savefig(
        #     self.data_path + "images/img_scatter_" + self.name + " - " + self.name + "_" + str(
        #         plots) + ".png")  # save the figure to file
        """
        idea
            plot con 4
            all'inizio tutti i puntini, ognuno con un colore diverso in base alla serie da cui proviene 
            poi provo a far la linea
        """

    def __scatter_plot(self, ax, data, ages):

        for series in data:
            ax.scatter(ages, series, label=series.name)  # mettere il nome della serie e le cose qui

        # Add a legend and axis labels
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')

