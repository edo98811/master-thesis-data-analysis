import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from scipy import stats
import seaborn as sns
import data_manipulation as dm
import numpy as np
from copy import deepcopy
import pingouin as pg
# from statsmodels.stats import shapiro
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
    modifiche importanti
        - fare diagramma del codice 
        - scrivere unittest
        - fare selezionare colonne
        - fare create table
        - raggruppare in funzioni quello che si puo 
        - ICC non serve
        - controllare bland altmann
        - aggiungere shapiro wilk
        - aggiungere il ciclo for e rendere la variabile data una tupla per tutti i plot
        - rendere la variabile plot nei plots globale
        - dividere tutti 

"""


class LogWriter:
    log_list = []
    save_file = "log.txt"

    @classmethod
    def clearlog(cls):
        with open(cls.save_file, 'w') as output:
            output.write(str("------new log") + '\n')

    @classmethod
    def log(cls, line):
        print(line)
        with open(cls.save_file, 'a') as output:
            output.write(str(line) + '\n')

    def __init__(self, save_file="log.txt"):
        with open(save_file, 'w') as output:
            for row in LogWriter.log_list:
                output.write(str(row) + '\n')

        print(f"log saved in {save_file}")


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

    def __init__(self, name, b_path, dataset_path="", p_path="", df_subj=None, d_folder="data_testing_ADNI/", table_file="", dataset="ADNI"):
        """
        :param name: str - name of the object
        :param b_path: str - base path
        :param p_path: str - path to check for processed images
        :param df_subj: pd.df the dataframe of subjects
        :param d_folder: str - data folder (default: data_testing/)
        """

        self.dataset = dataset
        if p_path:
            self.processed_path = p_path
        else:
            self.processed_path = ""
        self.dataset_path = dataset_path

        self.base_path = b_path
        self.data_path = b_path + d_folder
        self.name = name

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # definition of
        if df_subj is not None:
            self.df = df_subj
        else:
            self.df = self.create_table(table_file)

        self.subjects_list = self.df["ID"].tolist()

    def update(self):
        """
        function to update the table
        :return:
        """
        # for i, subj_path_filtered in enumerate(df["ID"].tolist()):
        #     subjs.add("sub-" + subj_path_filtered)

        # iterate though all the directories in the processed path
        if self.processed_path:
            for root, dirs, files in os.walk(self.processed_path):
                for dir in dirs:
                    if dir in self.subjects_list:
                        # quando trova il soggetto nella cartella modifica il dataframe
                        for i, subj_path_filtered in enumerate(self.df["ID"].tolist()):
                            if dir == "sub-" + subj_path_filtered:
                                self.df.loc[i, "processed"] = "yes"
                                self.df.loc[i, "processed_path"] = root + "/" + dir
                                break
        else:
            LogWriter.log("processed path empty")

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

    def create_table(self, origin_file, check_processed=True):
        """
        method to create the table if it doesn't exist
        :return:
        """

        table = pd.read_csv(self.base_path + origin_file)

        # create the dictionary that will turn into a table
        if self.dataset == "ADNI":
            df_dict = {
                "ID": [],
                "path": [],
                "age": [],
                "sex": [],
                "main_condition": [],
                "processed": [],
                "processed_path": []
            }
        elif self.dataset == "OASIS":
            df_dict = {
                "ID": [],
                "path": [],
                "age": [],
                "main_condition": [],
                "processed": [],
                "processed_path": []
            }
        elif self.dataset == "Portuguese":
            df_dict = {
                "ID": [],
                "path": [],
                "age": [],
                "main_condition": [],
                "processed": [],
                "processed_path": []
            }
        else:
            df_dict = {}

        _paths_on_table = []
        # extracts all the paths for the subjects
        if self.dataset == "ADNI" or self.dataset == "OASIS":
            IDs = Table.add_sub(table["ID"])
            _paths_in_folder = os.listdir(self.dataset_path)
            _paths_on_table = set(_paths_in_folder).intersection(Table.add_sub(IDs))

        if self.dataset == "Portuguese":
            root, dirs, files = os.walk(self.dataset_path)
            for file in files:
                _paths_on_table.append(f"{root}/{file}")

        # populates the dictionary
        # checks that subjects both exist in the table and on the computer
        # for that it needs to check the subdirectory of the subjects exists

        for index, row in table.iterrows():
            for i, path_on_table in enumerate(_paths_on_table):
                if len(path_on_table.split("/")) > 3:
                    if self.dataset == "ADNI" or self.dataset == "OASIS":
                        match = re.split("sub-", path_on_table.split("/")[-4])
                        if row["ID"] == match[1]:
                            if self.dataset == "ADNI" and (row["_merge"] == "both" or row["_merge"] == "right_only"):
                                df_dict["ID"].append(row["ID"])
                                df_dict["path"].append(path_on_table)
                                df_dict["age"].append(row["age"])
                                df_dict["sex"].append(row["sex"])
                                df_dict["main_condition"].append(row["diagnosis"])
                                df_dict["processed"].append("no")
                                df_dict["processed_path"].append("")
                            elif self.dataset == "ADNI":
                                df_dict["ID"].append(row["ID"])
                                df_dict["path"].append(path_on_table)
                                df_dict["age"].append(row["ageAtEntry"])
                                df_dict["main_condition"].append(row["dx1"])
                                df_dict["processed"].append("no")
                                df_dict["processed_path"].append("")
                        elif self.dataset == "Portuguese":
                            df_dict["ID"].append(row["PatientID"])
                            df_dict["path"].append(path_on_table)
                            df_dict["age"].append(row["((0010, 1010)-Patients Age)"])
                            df_dict["main_condition"].append("dementia")
                            df_dict["processed"].append("no")
                            df_dict["processed_path"].append("")

        df = pd.DataFrame.from_dict(df_dict)

        if check_processed == True:
            subjs = set()
            # checks the processed
            # interate though all the rows to create a set of the subjects
            for i, subj_path_filtered in enumerate(df["ID"].tolist()):
                df.loc[i, "processed"] = "no"
                subjs.add("sub-" + subj_path_filtered)

            # iterate though all the directories in the processed path
            for root, dirs, files in os.walk(self.processed_path):
                for dir in dirs:
                    if dir in subjs:
                        # quando trova il soggetto nella crtela modifica il dataframe
                        for i, subj_path_filtered in enumerate(df["ID"].tolist()):
                            if dir == "sub-" + subj_path_filtered:
                                df.loc[i, "processed"] = "yes"
                                df.loc[i, "processed_path"] = root + "/" + dir
                                break

        return df

    @staticmethod
    def add_sub(_list):
        """
        :param _list: list of str - list of subj names
        :return:
        """
        l = []
        for i, s in enumerate(_list):
            l.append("sub-" + s)
        LogWriter.log("    add_sub: correctly added sub- to all the patients")
        return l


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

    def __init__(self, name, b_path, df_subj_obj, query, d_folder="data_testing_ADNI/", aseg=None,
                 aparcLeft=None, aparcRight=None, alg="fast"):
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

        global plots_n
        plots_n = 0

        LogWriter.log(f"inizializing Stats for {name}")

        # here there is the df only already filtered
        if query:
            self.df_subj = df_subj_obj.get_query(query)

        self.subj_list = self.add_sub(self.df_subj["ID"].tolist())
        t = deepcopy(self.subj_list)

        # path definition and folder creation
        self.base_path = b_path
        self.data_path = self.base_path + d_folder

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # other important parameters
        self.query = query
        self.name = name
        self.alg = alg

        # add control that these data are dataframes
        if alg == "fast":
            if aparcLeft is not None:
                self.df_stats_aparcL = aparcLeft
                self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(t)]
            else:
                LogWriter.log(f"    extracting aparcL stats for {self.name}...")
                self.df_stats_aparcL = self.extract_stats_fast('rh.aparc.DKTatlas.mapped.stats', 1)
                self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(t)]
            if aparcRight is not None:
                self.df_stats_aparcR = aparcRight
                self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR["ID"].isin(self.subj_list)]
            else:
                LogWriter.log(f"    extracting aparcR stats for {self.name}...")
                self.df_stats_aparcR = self.extract_stats_fast('lh.aparc.DKTatlas.mapped.stats', 1)
                self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR["ID"].isin(t)]
            if aseg is not None:
                self.df_stats_aseg = aseg
                self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg["ID"].isin(t)]
            else:
                LogWriter.log(f"    extracting aseg stats for {self.name}...")
                self.df_stats_aseg = self.extract_stats_fast('aseg.stats', 0)
                self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg["ID"].isin(t)]
        if alg == "free":
            if aparcLeft is not None:
                self.df_stats_aparcL = aparcLeft
                self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(t)]
            else:
                LogWriter.log(f"    extracting aparcL stats for {self.name}...")
                self.df_stats_aparcL = self.extract_stats_free('rh.aparc.DKTatlas.stats', 1)
                self.df_stats_aparcL = self.df_stats_aparcL[self.df_stats_aparcL["ID"].isin(t)]
            if aparcRight is not None:
                self.df_stats_aparcR = aparcRight
                self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR["ID"].isin(self.subj_list)]
            else:
                LogWriter.log(f"    extracting aparcR stats for {self.name}...")
                self.df_stats_aparcR = self.extract_stats_free('lh.aparc.DKTatlas.stats', 1)
                self.df_stats_aparcR = self.df_stats_aparcR[self.df_stats_aparcR["ID"].isin(t)]
            if aseg is not None:
                self.df_stats_aseg = aseg
                self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg["ID"].isin(t)]
            else:
                LogWriter.log(f"    extracting aseg stats for {self.name}...")
                self.df_stats_aseg = self.extract_stats_free('aseg.stats', 0)
                self.df_stats_aseg = self.df_stats_aseg[self.df_stats_aseg["ID"].isin(t)]

        #
        # print(self.df_stats_aseg.head())
        # print("len sbj list" + str(len(self.subj_list)))
        # print(t)
        # print(len(self.df_stats_aseg["ID"].tolist()))
        # print(self.subj_list)
        # print(t)
        # print(self.df_stats_aseg["ID"].tolist())
        # self.subj_list = self.add_sub(self.subj_list)
        self.subj_list = [v for v in t if v in self.df_stats_aseg["ID"].tolist()]
        temp = set(self.delete_sub(t))
        self.df_subj = self.df_subj[self.df_subj["ID"].isin(temp)]
        self.n_sub = len(self.df_subj)

        if self.n_sub > 0:
            LogWriter.log(f"stats {self.name} correctly initialized {self.n_sub} being considered")
            LogWriter.log(f"    len aseg {len(self.df_stats_aseg)}")
            LogWriter.log(f"    len aparcR {len(self.df_stats_aparcL)}")
            LogWriter.log(f"    len aparcR {len(self.df_stats_aparcR)}")
        else:
            LogWriter.log(f"stats {self.name} EMPTY")
        # print(len(self.subj_list))
        # print(self.subj_list[0])

    @staticmethod
    def add_sub(_list):
        """
        :param _list: list of str - list of subj names
        :return:
        """
        l = []
        for i, s in enumerate(_list):
            l.append("sub-" + s)
        LogWriter.log("    add_sub: correctly added sub- to all the patients")
        return l

    @staticmethod
    def delete_sub(_list):
        """
        :param _list:
        :param _list: list of str - list of subj names
        :return:
        """
        l = []
        for i, s in enumerate(_list):
            match = re.split("sub-", s)
            if len(match) > 1:
                l.append(match[1])
        if len(l) != len(_list):
            LogWriter.log("warning deletesub: wrong number of subjects matched the pattern sub-#######...")
        else:
            LogWriter.log("    delete_sub: correctly deleted sub- from all the patients")
        return l

    def extract_stats_fast(self, stats_filename, _type):
        """
        :param stats_filename: str
        :param _type: int aseg or aparc (0 or 1)
        :return:
        """
        stat_df_paths = self.__extract_path(stats_filename)
        # print("len stat paths found :" + str(len(stat_df_paths)))
        # LogWriter.log("len stat paths found :" + str(len(stat_df_paths)))

        if stat_df_paths:

            # print(f"stats file {stats_filename} found for {str(len(stat_df_paths))} subjects")
            LogWriter.log(f"stats file {stats_filename} found for {str(len(stat_df_paths))} subjects")

            if _type == 0:
                # __(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__fast_stats_aseg(stat_df_paths)
            elif _type == 1:
                # stats_aparcDTK(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__fast_stats_aparcDTK(stat_df_paths)
        else:
            # print(f"no stat file: {stats_filename} found in paths on table")
            LogWriter.log(f"no stat file: {stats_filename} found in paths on table")

    def extract_stats_free(self, stats_filename, _type):
        """
        :param stats_filename: str
        :param _type: int aseg or aparc (0 or 1)
        :return:
        """
        stat_df_paths = self.__extract_path(stats_filename)

        if stat_df_paths:
            # print(f"stats file {stats_filename} found for {str(len(stat_df_paths))} subjects")
            LogWriter.log(f"stats file {stats_filename} found for {str(len(stat_df_paths))} subjects")
            if _type == 0:
                # __(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__free_stats_aseg(stat_df_paths)
            elif _type == 1:
                # stats_aparcDTK(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.__free_stats_aparcDTK(stat_df_paths)
        else:
            # print(f"no stat file: {stats_filename} found in paths on table")
            LogWriter.log(f"no stat file: {stats_filename} found in paths on table")

    def save_stats_files(self, which=(True, True, True), names=("aseg.csv", "aparcDKT_right.csv", "aparcDKT_left.csv")):
        """
        :param which: tuple of bool - which files to save (default: True, True, True)
        :param names: tuple - names of the files (default: "aseg.csv", "aseg_right.csv", "aseg_left.csv")
        :return:
        """
        path = self.data_path + self.name + "_stats"
        if not os.path.exists(path):
            os.makedirs(path)

        if which[0]:
            self.df_stats_aseg.to_csv(path + "/" + names[0])
        if which[1]:
            self.df_stats_aparcL.to_csv(path + "/" + names[1])
        if which[2]:
            self.df_stats_aparcR.to_csv(path + "/" + names[2])

    @staticmethod
    def __fast_stats_aseg(subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # LogWriter.log("     extracting stats for subject " + str(n + 1) + ", path:" + path)

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
        # print(str(df_dict))
        return pd.DataFrame.from_dict(df_dict, orient='columns')

    @staticmethod
    def __fast_stats_aparcDTK(subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # LogWriter.log("     extracting stats for subject " + str(n + 1) + ", path:" + path)

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

    @staticmethod
    def __free_stats_aseg(subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # LogWriter.log("     extracting stats for subject " + str(n + 1) + ", path:" + path)

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

    @staticmethod
    def __free_stats_aparcDTK(subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            # LogWriter.log("     extracting stats for subject " + str(n + 1) + ", path:" + path)

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
        subj_list_numbers = set(self.delete_sub(self.subj_list))
        # creates a list with all the subjects that are in the list
        # for s in subj_list:
        #     if len(s.split("/")) > 4:
        #         subj_list_numbers.add(s.split("/")[-4])
        # print(subj_list_numbers)
        # to be updated for every processed paths
        # paths_found = []
        # for path, subdirs, files in os.walk(self.processed_path):
        #     if path.split("/")[-1] == 'stats' and path.split("/")[-2] in subj_list_numbers:
        #         for name in files:
        #             if name == filename:
        #                 paths_found.append(path + "/" + name)
        #
        # if not paths_found:
        #     return False
        #
        # return paths_found

        # seconda parte da fare
        paths_found = []
        if self.alg == "fast":
            for s in subj_list_numbers:
                # list_path = str(self.df_subj[self.df_subj["ID"] == s]["processed_path"])
                # str_path = "/".join(list_path[:-1])
                # print(s)
                s_path = str(self.df_subj[self.df_subj["ID"] == s]["processed_path"].iloc[0])
                # print(s_path)

                for path, subdirs, files in os.walk(s_path):
                    if path.split("/")[-1] == "stats":  # and path.split("/")[-2] in subj_list_numbers:
                        for name in files:
                            if name == filename:
                                paths_found.append(path + "/" + name)
        elif self.alg == "free":
            for s in subj_list_numbers:
                # list_path = str(self.df_subj[self.df_subj["ID"] == s]["processed_path"])
                # str_path = "/".join(list_path[:-1])
                # print(s)
                s_path = str(self.df_subj[self.df_subj["ID"] == s]["path"].iloc[0])
                s_path = "/".join(s_path.split("/")[:-3])
                # print(s_path)

                for path, subdirs, files in os.walk(s_path):
                    if path.split("/")[-1] == "stats":  # and path.split("/")[-2] in subj_list_numbers:
                        for name in files:
                            if name == filename:
                                paths_found.append(path + "/" + name)
            # for s in self.subj_list:
            #     s_path = os.path.dirname(self.df_subj[self.df_subj["ID"] == s]["path"][:-2])
            #
            #     for path, subdirs, files in os.walk(s_path):
            #         if path.split("/")[-1] == "stats":  # and path.split("/")[-2] in subj_list_numbers:
            #             for name in files:
            #                 if name == filename:
            #                     paths_found.append(path + "/" + name)
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

    def __init__(self, name, b_path, stats_df_1, stats_df_2, alpha=0.05, d_folder="data_testing_ADNI/",
                 columns_to_test=None,
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

        # definition of the objects to compare
        if isinstance(stats_df_1, Stats):
            self.stat_df_1 = stats_df_1
        else:
            raise "stats of the wrong class"
        if isinstance(stats_df_2, Stats):
            self.stat_df_2 = stats_df_2
        else:
            raise "stats of the wrong class"

        # definition od path variables and folders
        self.base_path = b_path

        self.data_path = self.base_path + d_folder
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        # create common subjects list and common column list
        self.subjects_list = set(self.stat_df_1.df_subj["ID"].tolist()).intersection(
            set(self.stat_df_2.df_subj["ID"].tolist()))
        self.columns_list = set(self.stat_df_1.df_subj.columns.tolist()).intersection(
            set(self.stat_df_2.df_subj.columns.tolist()))

        # check that there are common subjects and define image path
        if not self.subjects_list or not self.columns_list:
            raise "datasets do not have elements in common"
        if not os.path.exists(self.data_path + "images/"):
            os.makedirs(self.data_path + "images/")

        # create the common
        # self.subjects_list = set(stats_df_2.add_sub(list(self.subjects_list)))

        # other important variables
        self.name = name
        self.alpha = alpha
        self.updated_alpha = "no correction"
        self.max_plot = max_plot

        self.stat_df_result = None
        global plots
        plots = 0
        # creation of the statistical test variables (can be deleted)
        # self.stat_test(columns_to_test)

    def violin(self, data=("aseg", "aparcL", "aparcR"), columns=None, n_subplots=10, n_rows=2, c_to_exclude=[]):

        """
        :param data: str - table to select (aseg, aparcL, aparcR)
        :param columns: list  of str- list of column names to print (default None: prints all)
        :param n_subplots: int - n of subplots in image (default 4)
        :param n_rows: int - n of rows in plot (default 2)
        :return: void
        """

        LogWriter.log(f"Violin plot: {self.name}")

        for d in data:
            _df1, _df2 = self.get_data(d)

            LogWriter.log(f"    length of the tables to compare {len(_df1)} {len(_df2)}")

            # if not columns:
            #     columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))

            not_done = []
            for column_to_compare in self.columns_list:
                if column_to_compare not in c_to_exclude:
                    a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                    b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')

                    if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):

                        if not plots % n_subplots:
                            if plots > 1:
                                fig.savefig(f"{self.data_path}images/img_{data}_violin_{self.name}"
                                            f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
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
                        # print(index)
                        self.__violin_plot(axs[index], a, b, title=a.name + "\n" + self.name)
                        plots += 1
                    else:
                        not_done.append(a.name)

                    if plots >= self.max_plot:  # to avoid plotting too much
                        break
                else:
                    LogWriter.log(f"excluded {column_to_compare}")

            if plots % n_subplots != 0:
                fig.savefig(f"{self.data_path}images/img_{data}_violin_{self.name}"
                            f"_{str(plots - (plots % n_subplots))}-{str(plots)}.png")  # save the figure to file
            del axs, fig

        LogWriter.log(f"    plotted for {plots} variables out of {len(columns)}")
        not_done_str = ' | '.join(not_done)
        LogWriter.log(f"    skipped: {not_done_str}")

    def bland_altmann(self, data=("aseg", "aparcL", "aparcR"), columns=None, n_subplots=4, n_rows=2, c_to_exclude=[]):
        """
        :param data: str - table to select (aseg, aparcL, aparcR)
        :param columns: list  of str- list of column names to print (default None: prints all)
        :param n_subplots: int - n of subplots in image (default 4)
        :param n_rows: int - n of rows in plot (default 2)
        :return: void
        """

        LogWriter.log(f"Bland altmann plot: {self.name}")
        for d in data:
            _df1, _df2 = self.get_data(d)

            # print(f"BA length of the tables to compare {len(_df1)} {len(_df2)}")
            LogWriter.log(f"    BA length of the tables to compare {len(_df1)} {len(_df2)}")

            # if c_to_exclude:
            #     LogWriter.log(f"    excluding {len(c_to_exclude)} columns ")
            #     for c in c_to_exclude:
            #         if c in self.columns_list:
            #             _df1 = _df1.drop(c, axis=1)
            #             _df2 = _df2.drop(c, axis=1)
            #             LogWriter.log(f"        {c} deleted")

            # checks that the subjects to compare are the same
            # if len(_df1) != len(_df2):
            #     LogWriter.log(f"    correction, selection of common subjects")
            #
            #     set1 = set(_df1.loc[:, "ID"].tolist())
            #     set2 = set(_df2.loc[:, "ID"].tolist())
            #
            #     sd = set1.symmetric_difference(set2)
            #     LogWriter.log(f"        elements to delete: {' '.join(sd)}")
            #     for id_to_delete in sd:
            #         if id_to_delete in set1:
            #             LogWriter.log(f"            element{id_to_delete} found in  {self.stat_df_1.name}")
            #             _df1 = _df1[_df1["ID"] != id_to_delete]
            #             LogWriter.log(f"            dropped: {id_to_delete} from {self.stat_df_1.name}")
            #         else:
            #             LogWriter.log(f"            element{id_to_delete} found in  {self.stat_df_2.name}")
            #             _df2 = _df2[_df2["ID"] != id_to_delete]
            #             LogWriter.log(f"            dropped: {id_to_delete} from {self.stat_df_2.name}")
            # _df1, _df2 = self.__match_dataframes(_df1, _df2)
            # create set of common fields, to be deleted

            self.__match_dataframes(_df1, _df2)
            # if not columns:
            #     columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))  # set with columns

            # iterates through the columns
            not_done = []
            for column_to_compare in self.columns_list:
                if column_to_compare not in c_to_exclude:

                    a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                    b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')
                    # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
                    if a.any() and b.any() and (
                            a.notnull().all() and b.notnull().all()):  # for all the fields with numbers

                        if not plots % n_subplots:
                            if plots > 1:
                                fig.savefig(f"{self.data_path}images/img_{d}_ba_{self.name}"
                                            f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
                                # handles, labels = ax.get_legend_handles_labels()
                                # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
                            fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
                            axs = axs.ravel()
                            plt.subplots_adjust(hspace=0.5)
                            plt.subplots_adjust(wspace=0.2)

                        index = plots % n_subplots

                        self.__bland_altman_plot(axs[index], a, b, title=a.name + "\n" + self.name)
                        plots += 1
                    else:
                        not_done.append(a.name)
                    if plots >= 20:  # to avoid plotting too much
                        break
                else:
                    LogWriter.log(f"excluded {column_to_compare}")

            if plots % n_subplots != 0:
                fig.savefig(f"{self.data_path}images/img_{d}_ba_{self.name}"
                            f"_{str(plots - (plots % n_subplots))}-{str(plots)}.png")  # save the figure to file
            del axs, fig

        LogWriter.log(f"    plotted {plots} variables out of {len(columns)}")
        not_done_str = ' | '.join(not_done)
        LogWriter.log(f"    skipped: {not_done_str}")

    def get_data(self, data):
        if data == "aseg":
            _df1 = self.stat_df_1.df_stats_aseg[self.stat_df_1.df_stats_aseg["ID"].isin(self.subjects_list)]
            _df2 = self.stat_df_2.df_stats_aseg[self.stat_df_2.df_stats_aseg["ID"].isin(self.subjects_list)]
        elif data == "aparcR":
            _df1 = self.stat_df_1.df_stats_aparcL[self.stat_df_1.df_stats_aparcL["ID"].isin(self.subjects_list)]
            _df2 = self.stat_df_2.df_stats_aparcL[self.stat_df_2.df_stats_aparcL["ID"].isin(self.subjects_list)]
        elif data == "aparcL":
            _df1 = self.stat_df_1.df_stats_aparcR[self.stat_df_1.df_stats_aparcR["ID"].isin(self.subjects_list)]
            _df2 = self.stat_df_2.df_stats_aparcR[self.stat_df_2.df_stats_aparcR["ID"].isin(self.subjects_list)]
        else:
            raise "wrong selection parameter"

        return _df1, _df2

    def bland_altmann_column(self, data=("aseg", "aparcL", "aparcR"), columns=None, n_subplots=4, n_rows=2,
                             c_to_exclude=[]):
        LogWriter.log("BLAND ALTMANN")
        for d in data:
            df1, df2 = self.get_data(d)

            self.iterate_columns(self.__bland_altman_plot)

    def iterate_columns(self, function, n_rows, n_subplots, plot_title, c_to_exclude, _df1, _df2):

        not_done = []
        for column_to_compare in self.columns_list:
            if column_to_compare not in c_to_exclude:
                a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')

                if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):

                    if not plots % n_subplots:
                        if plots > 1:
                            fig.savefig(f"{plot_title}"
                                        f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
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
                    # print(index)
                    function(axs[index], a, b, title=a.name + "\n" + self.name)

                    plots += 1
                else:
                    not_done.append(a.name)

                if plots >= self.max_plot:  # to avoid plotting too much
                    break
            else:
                LogWriter.log(f"excluded {column_to_compare}")

        if plots % n_subplots != 0:
            fig.savefig(f"{plot_title}"
                        f"_{str(plots - (plots % n_subplots))}-{str(plots)}.png")  # save the figure to file
        del axs, fig

    def stat_test(self, columns_input=None, data=("aseg", "aparcL", "aparcR")):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :return: void
        """
        r_all = []
        for data_n in data:
            if data_n == "aseg":
                _df1 = self.stat_df_1.df_stats_aseg
                _df2 = self.stat_df_2.df_stats_aseg
            elif data_n == "aparcR":
                _df1 = self.stat_df_1.df_stats_aparcL
                _df2 = self.stat_df_2.df_stats_aparcL
            elif data_n == "aparcL":
                _df1 = self.stat_df_1.df_stats_aparcR
                _df2 = self.stat_df_2.df_stats_aparcR
            else:
                raise "stat_test: wrong selection parameter"

            LogWriter.log(f"t_test and mann whitney on {data_n} in {self.name}...")

            # se non viene dato un input fa il test per tutte le colonne
            if not columns_input:
                columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))
            else:
                columns = columns_input
            # if not columns:
            #     columns = _df1.columns
            #     columns.intersection(_df2_filtered.columns).tolist()
            # if not columns:
            #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
            #     columns = range(2, max_len)
            not_done = []
            for i, column_to_compare in enumerate(columns):
                a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')

                if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                    # print(
                    #   f"performing statistical analysis for data in category {column_to_compare}for file {self.name} - {data}")
                    # LogWriter.log(
                    #    f"      performing statistical analysis for data in category {column_to_compare} for file {self.name} - {data_n}")

                    r1, p1, o1 = self.__mann_whitney(a, b)
                    r2, p2, o2 = self.__t_test(a, b)
                    d, rd = self.__cohens_d(a, b)
                    # ICC

                    if isinstance(column_to_compare, int):
                        column_to_compare_name = _df1.columns[column_to_compare]

                        r_all.append({"name": f"{self.name}_{data_n}_{column_to_compare_name}",
                                      "mann_whitney": {"result": r1,
                                                       "p_value": p1,
                                                       "outcome": o1},
                                      "t_test": {"result": r2,
                                                 "p_value": p2,
                                                 "outcome": o2},
                                      "d": {"result": rd,
                                            "d_value": d}})

                    if isinstance(column_to_compare, str):
                        r_all.append({"name": f"{self.name}_{data_n}_{column_to_compare}",
                                      "mann_whitney": {"result": r1,
                                                       "p_value": p1,
                                                       "outcome": o1},
                                      "t_test": {"result": r2,
                                                 "p_value": p2,
                                                 "outcome": o2},
                                      "d": {"result": rd,
                                            "d_value": d}})

                else:
                    # print(f"absent or not valid data in category {column_to_compare}for file {self.name} - {data}")
                    not_done.append(column_to_compare)

            LogWriter.log(f"    tested {i} variables out of {len(columns)}")
            not_done_str = '         \n '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")
        self.__save_dataframe(r_all)

    def bonferroni_correction(self, save=False):
        """
        :param save: bool - if true save the file after correction
        :return: void
        """

        self.updated_alpha = self.__correction_param()

        # iterates through the rows od the table and applies the correction
        for i, row in self.stat_df_result.iterrows():
            if type(row["mann_whitney p_value"]) is not str and type(row["mann_whitney p_value"]) is not str and type(
                    self.updated_alpha) is not str:
                if row["mann_whitney p_value"] < self.updated_alpha:
                    row[
                        "mann_whitney message"] = f"p-value: {row['mann_whitney p_value']} - null hypothesis " \
                                                  f"rejected, means are not statistically equal "
                    row["mann_whitney outcome"] = 1
            if type(row["t_test p_value"]) is not str and type(row["t_test p_value"]) is not str and type(
                    self.updated_alpha) is not str:
                if row["t_test p_value"] < self.updated_alpha:
                    row[
                        "t_test message"] = f"p-value: {row['t_test p_value']} - null hypothesis rejected, the " \
                                            f"datasets have a different distribution "
                    row["t_test outcome"] = 1
            row.loc["alpha_correction"] = self.updated_alpha
            if len(row) == len(self.stat_df_result.loc[i, :]):
                self.stat_df_result.loc[i, :] = row
            else:
                LogWriter.log(
                    f"     row{i} ERROR BONFERRONI CORRECTION, follows row from dataframe and row processed")
                LogWriter.log(self.stat_df_result.loc[i, :])
                LogWriter.log(row.tolist())

            if save:
                self.stat_df_result.to_csv(self.data_path + f"{self.name}_bonferroni_corrected.csv")

    def save_data(self, filename=None):
        """
        to csv in basepath + filename
        :param filename: str - name of the file to be saved into
        :return:
        """
        if filename is None:
            filename = f"{self.name}_stats.csv"
        self.stat_df_result.to_csv(self.data_path + filename)

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

    @staticmethod
    def __t_test(_a, _b):
        # a, b = get_column(column_to_compare, df1, df2)

        # togliere questo
        if "NaN" in _a or "NaN" in _b:
            print("could not compute")
            return "result could not be computed", "NaN", "NaN"

        t_stat, p_value = stats.ttest_ind(_a, _b)

        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected"
            outcome = 1

        return result, p_value, outcome

    @staticmethod
    def __mann_whitney(_a, _b):
        # a, b = get_column(column_to_compare, df1, df2)

        if "NaN" in _a or "NaN" in _b:
            return "result could not be computed", "NaN", "NaN"

        # df1.to_csv("dataset_uniti_test.csv", index=False)

        # t_stat, p_value = stats.mannwhitneyu(_a, _b)
        t_stat, p_value = stats.wilcoxon(_a, _b)

        # p value is the likelihood that these are the same
        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected"
            outcome = 1

        return result, p_value, outcome

    @staticmethod
    def __cohens_d(_a, _b):
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

    # @staticmethod
    # def __ICC(_a, _b):
    #     """
    #     Calculates the Intraclass Correlation Coefficient (ICC) between two methods
    #     that are passed as pandas series.
    #     """
    #     # Calculate the mean of the two series
    #     mean = (series1.mean() + series2.mean()) / 2
    #
    #     # Calculate the sum of squares between and within the two series
    #     ss_between = ((series1.mean() - mean) ** 2 + (series2.mean() - mean) ** 2) * len(series1)
    #     ss_within = ((series1 - series2) ** 2).sum()
    #
    #     # Calculate the total sum of squares
    #     ss_total = ((series1 - mean) ** 2 + (series2 - mean) ** 2).sum()
    #
    #     # Calculate the ICC using the formula:
    #     # ICC = (SS_between - SS_within) / (SS_total + SS_within)
    #     icc = (ss_between - ss_within) / (ss_total + ss_within)
    #
    #     return icc

    @staticmethod
    def __violin_plot(_ax, _a, _b, title):
        # Create a DataFrame with the two Series
        # df = pd.DataFrame({'Freesurfer': _a, 'Fastsurfer': _b})
        df = pd.DataFrame({'Data': pd.concat([_a, _b]),
                           'Group': ['FreeSurfer'] * len(_a) + ['FastSurfer'] * len(_b),
                           "Area": [_a.name] * (len(_a) + len(_b))})

        # Create a split violin plot
        # sns.violinplot(data=df, split=True)
        sns.violinplot(ax=_ax, data=df, hue="Group", x="Area", y="Data", split=True)
        _ax.title.set_text(title)
        _ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        # ax.yaxis.set_major_formatter(plt.FormatStrFormatter('{:.3g}'))
        _ax.set_xlabel("")

    @staticmethod
    def __bland_altman_plot(_ax, _a, _b, title):
        # Compute mean and difference between two series
        mean_list = []
        # print(f"{len(_a)} {len(_b)}")
        # if len(_a) != len(_b):
        #     print("arrays have different lenghts")
        #     LogWriter.log_list.append("arrays have different length")
        #     LogWriter.log_list.append(_b.tolist())
        #     LogWriter.log_list.append(_a.tolist())
        #     return
        # for i, (a, b) in enumerate(zip(_a, _b)):
        #     mean_list.append((a + b) / 2)
        mean = np.mean([np.array(_a), np.array(_b)], axis=0)
        # mean = np.array(mean_list)
        diff = np.array(_a) - np.array(_b)
        # print(f"{len(mean)} {mean}")
        # print(f"{len(diff)} {diff}")
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
        _ax.set_title(title)  # query.split("=")[-1])
        _ax.legend(['Mean difference', '95% limits of agreement'])
        _ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0), useMathText=True)
        _ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)

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

    def __match_dataframes(self, df1, df2):
        LogWriter.log(f"    subject matching")
        LogWriter.log(f"    selection of common subjects")

        set1 = set(df1.loc[:, "ID"].tolist())
        set2 = set(df2.loc[:, "ID"].tolist())

        sd = set1.symmetric_difference(set2)
        u = set1.intersection(set2)

        if sd:
            LogWriter.log(f"        elements to delete: {' '.join(sd)}")
            for id_to_delete in sd:
                if id_to_delete in set1:
                    LogWriter.log(f"            element{id_to_delete} found in  {self.stat_df_1.name}")
                    df1 = df1[df1["ID"] != id_to_delete]
                    LogWriter.log(f"            dropped: {id_to_delete} from {self.stat_df_1.name}")
                if id_to_delete in set2:
                    LogWriter.log(f"            element{id_to_delete} found in  {self.stat_df_2.name}")
                    df2 = df2[df2["ID"] != id_to_delete]
                    LogWriter.log(f"            dropped: {id_to_delete} from {self.stat_df_2.name}")
        else:
            LogWriter.log(f"        no element to delete")

        LogWriter.log(f"    subject matching...")

        # sorts the dataframe by subject to make sure it has the same subjects
        df1.sort_index(inplace=True)
        df2.sort_index(inplace=True)

        # return df1, df2
        # a = np.array(len(u))
        # b = np.array(len(u))
        #
        # for i,subject in enumerate(u):
        #
        #     a[i] =
        #     b[i] =
        #
        # return a, b

    @staticmethod
    def saphiro_test(data):
        pass
        #
        # #t_stat, p_value = shapiro(data)
        #
        # #
        # if p_value > 0.05:
        #     result = f"p-value: {p_value} "
        #     outcome = 0
        # else:
        #     result = f"p-value: {p_value} "
        #     outcome = 1
        #
        # return result, p_value, outcome


class SummaryPlot:
    def __init__(self, name, b_path, stats_df_list, d_folder="data_testing_ADNI/", max_plot=500):
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

        self.name = name
        self.max_plot = max_plot
        # self.columns_list =

        global plots
        plots = 0

    # in teoria dovrei filtrarla prima
    def comparison_plot(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=["ID"], n_subplots=4, n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """

        df_list = []
        subj_lists = []
        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f" scatter plot:{self.name}...")
        for d in data:
            if d == "aseg":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aseg)
                    subj_lists.append(table.df_stats_aseg["ID"].tolist())
            elif d == "aparcR":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aparcL)
                    subj_lists.append(table.df_stats_aparcL["ID"].tolist())
            elif d == "aparcL":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aparcR)  # table
                    subj_lists.append(table.df_stats_aparcR["ID"].tolist())

            # creates the age series, to move up
            ages = []
            legend = []
            for table, subj_list in zip(self.df_list_obj, subj_lists):
                s = list(Stats.delete_sub(subj_list))
                t = table.df_subj[table.df_subj['ID'].isin(s)]
                a = t.loc[:, "age"].tolist()
                ages.append(pd.to_numeric(a, errors='coerce'))
                # legend.append(table.name)
            del a, t, s
            columns = df_list[0].columns
            # columns = columns.intersection(_df2.columns).tolist()
            # if not columns:
            #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
            #     columns = range(2, max_len)
            not_done = []
            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    title = f"{d} {column_to_compare}"
                    serieses = []
                    # selects the column from all the dataframes and puts them in a list of series
                    for i, df in enumerate(df_list):
                        series = pd.to_numeric(df[column_to_compare], errors='coerce')
                        series.rename(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
                        legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
                        LogWriter.log(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}. "
                                      f"series name {series.name}")
                        LogWriter.log(f"{legend[-1]}")

                        if series.any() and series.notnull().all():
                            serieses.append(series)
                            # print(f"ages {len(ages[i])}  - {type(ages[i])} {ages[i]}")
                            # print(f" series {len(serieses[i])} - {type(serieses[i].tolist())} {serieses[i].tolist()}")
                        else:
                            # print(series)
                            LogWriter.log(f"    comparison not possible for column {column_to_compare}")
                            not_done.append(column_to_compare)
                            break
                    if not len(serieses):
                        continue

                    # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
                    # if it needs to create a new figure it creates it
                    if not plots % n_subplots:
                        if plots > 1:
                            fig.savefig(f"{self.data_path}images/img_{d}_scatter_{self.name}"
                                        f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
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
                    index = plots % n_subplots
                    # print(index)
                    self.__scatter_plot(axs[index], serieses, ages, title, legend)
                    plots += 1

                    if plots >= self.max_plot:  # to avoid plotting too much
                        break

            if plots % n_subplots != 0:
                fig.savefig(f"{self.data_path}images/img_{d}_scatter_{self.name}"
                            f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
        del axs, fig

        LogWriter.log(f"    plotted {plots} variables out of {len(columns)}")
        not_done_str = ' | '.join(not_done)
        LogWriter.log(f"    skipped: {not_done_str}")
        # fig.savefig(
        #     self.data_path + "images/img_{data_scatter_" + self.name + " - " + self.name + "_" + str(
        #         plots) + ".png")  # save the figure to file
        """
        idea
            plot con 4
            all'inizio tutti i puntini, ognuno con un colore diverso in base alla serie da cui proviene 
            poi provo a far la linea
        """

    @staticmethod
    def __scatter_plot(ax, data, ages, title, legend):
        max_ = 0
        for series, age, legend_entry in zip(data, ages, legend):
            ax.scatter(age, series.tolist(), label=legend_entry)  # mettere il nome della serie e le cose qui
            LogWriter.log(series.name)
            if series.max() > max_:
                max_ = series.max()

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    def comparison_plot_line(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=["ID"], n_subplots=4, n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """

        df_list = []
        subj_lists = []

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f" scatter plot:{self.name}...")

        for d in data:
            plots = 0
            if d == "aseg":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aseg)
                    subj_lists.append(table.df_stats_aseg["ID"].tolist())
            elif d == "aparcR":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aparcL)
                    subj_lists.append(table.df_stats_aparcL["ID"].tolist())
            elif d == "aparcL":
                for table in self.df_list_obj:
                    df_list.append(table.df_stats_aparcR)  # table
                    subj_lists.append(table.df_stats_aparcR["ID"].tolist())

            # creates the age series, to move up
            legend = []
            # creates ages list with all the subjects in the lists
            # for table, subj_list in zip(self.df_list_obj, subj_lists):

            # legend.append(table.name)

            # creates column list if it doesnt exist
            columns = df_list[0].columns
            # add this method for creating the column list
            # self.columns_list = set(self.stat_df_1.df_subj.columns.tolist()).intersection(
            #     set(self.stat_df_2.df_subj.columns.tolist()))
            # columns = columns.intersection(_df2.columns).tolist()
            # if not columns:
            #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
            #     columns = range(2, max_len)
            not_done = []
            # idea: for each column you create another dataset with only the average and not the single subjects
            data_points_list = []

            for table, subj_list, df_element in zip(self.df_list_obj, subj_lists, df_list):
                df_element = df_element.set_index("ID")
                s = list(Stats.delete_sub(subj_list))
                t = table.df_subj[table.df_subj['ID'].isin(s)]
                ages = t.loc[:, "age"]
                ages.index = subj_list
                # ages.append(pd.to_numeric(a, errors='coerce'))

                # check if the indexes of the series are actually the subjects data
                full_table = pd.concat([df_element, ages], axis=1)
                age_groups = np.arange(55, 90, 5)

                # Create a new DataFrame to store the results
                full_table['AgeGroup'] = pd.cut(full_table['age'], bins=age_groups, labels=age_groups[:-1])
                # data_points = full_table.groupby('AgeGroup')[full_table.mean()]
                data_points = full_table.groupby('AgeGroup').mean()
                data_points.index = age_groups[:-1]

                # print(data_points.head())
                data_points_list.append(data_points)

                del t, s
                # add the lists of the confidence intervals, i need to calculate them like this and when i cut the dataframe, and sae themmaybe in ot
                # other two dataframes then i need to add them into the original dataframes
                # i could also do it after when i select the data, i mean the dataframes are still saved
                # se = np.std(y) / np.sqrt(len(y))
                # ci = 1.96 * se
                # data_points_cin = series + ci
                # data_points_cip = series - ci

                # idea: copiare cme ho fatto su comparisons
            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:

                    LogWriter.log(f"doing column{column_to_compare}")
                    title = f"{d} {column_to_compare}"
                    serieses = []

                    # selects the column from all the dataframes and puts them in a list of series
                    for i, df in enumerate(data_points_list):

                        # creation of the serieses to plot and ages
                        series = pd.to_numeric(df[column_to_compare], errors='coerce')
                        series.rename(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
                        legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
                        LogWriter.log(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}. "
                                      f"series name {series.name}")
                        LogWriter.log(f"{legend[-1]}")

                        if series.any() and series.notnull().all():
                            serieses.append(series)
                            # print(f"ages {len(ages[i])}  - {type(ages[i])} {ages[i]}")
                            # print(f" series {len(serieses[i])} - {type(serieses[i].tolist())} {serieses[i].tolist()}")
                        else:
                            # print(series)
                            LogWriter.log(f"        scatter not possible for column {column_to_compare}")
                            print(f"        scatter not possible for column {column_to_compare}")
                            not_done.append(column_to_compare)
                            break

                    if not len(serieses):
                        continue

                    # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
                    # if it needs to create a new figure it creates it
                    if not plots % n_subplots:
                        if plots > 1:
                            fig.savefig(f"{self.data_path}images/img_{d}_scatter_{self.name}"
                                        f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
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
                    index = plots % n_subplots
                    # print(index)
                    self.__line_plot(axs[index], serieses, age_groups[:-1], title, legend)
                    plots += 1

                    if plots >= self.max_plot:  # to avoid plotting too much
                        break

            if plots % n_subplots != 0:
                fig.savefig(f"{self.data_path}images/img_{d}_scatter_{self.name}"
                            f"_{str(plots - n_subplots)}-{str(plots)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")

    @staticmethod
    def __line_plot(ax, data, ages, title, legend):
        max_ = 0

        LogWriter.log("line plot")
        for series, age, legend_entry in zip(data, ages, legend):
            ax.plot(series.index.tolist(), series.tolist(),
                    label=legend_entry)  # mettere il nome della serie e le cose qui
            LogWriter.log(series.name)
            if series.max() > max_:
                max_ = series.max()

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)
