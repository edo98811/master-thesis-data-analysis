"""
cose da fare

- aggiungere in Stats una variabile columns per ogni dataframe



"""
"""
ATTRIBUTES STATS

self.df_subj_obj = df_subj_obj
self.df_subj = df_subj_obj.get_query(query)

global plots_n_n - DA CANCELLARE

self.subj_list = self.add_sub(self.df_subj["ID"].tolist()) (FILTERED) 
self.base_path = b_path
self.data_path = self.base_path + d_folder
self.query = query
self.name = name
self.alg = alg

        self.df_stats_aparcL
        self.df_stats_aparcR
        self.df_stats_aseg

self.n_sub = len(self.df_subj)

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

