import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from scipy import stats
import seaborn as sns
import data_manipulation as dm

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

    def __init__(self, df_subj, p_path, b_path):
        self.df = df_subj
        self.processed_path = p_path
        self.subjects_list = self.df["ID"].tolist()
        self.base_path = b_path

    def get_query_list(self, query):
        """
        old

        :param query:
        :return:
        """
        subjects_list = self.df.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s

        self.subjects_list = set(subjects_list)

    def update(self):
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

    def get_query(self, query, sub=False, only_processed=False):
        print (self.df.head())
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
            df = df.query("processed==yes")
        return df

    def save_csv(self, filename):

        """
        to csv in basepath + filename
        :param filename:
        :return:
        """
        self.df.to_csv(self.base_path + filename)

    # def add_sub(self, subjects_list):
    #     for i, s in enumerate(subjects_list):
    #         subjects_list[i] = "sub-" + s
    #     return subjects_list


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

    def __init__(self, df_subj, name, b_path, query, aseg=False, aparcLeft=False, aparcRight=False):

        self.subj_df_obj = df_subj

        self.subj_df = df_subj.get_query(query)
        self.subj_list = self.add_sub(self.subj_df["ID"].tolist())

        self.base_path = b_path
        # if not query or (not aseg or not aparcLeft or not aparcRight):
        #     raise " non va bene"
        self.data_path = self.base_path + "/data_testing"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.query = query
        self.name = name

        if aparcLeft:
            self.df_stats_aparkL = aparcRight
        else:
            self.df_stats_aparkL = self.save_stats('rh.aparc.DKTatlas.stats', 1)
        if aparcRight:
            self.df_stats_aparkR = aparcLeft
        else:
            self.df_stats_aparkR = self.save_stats('lh.aparc.DKTatlas.stats', 1)
        if aseg:
            self.df_stats_aseg = aseg
        else:
            self.df_stats_aseg = self.save_stats('aseg.stats', 0)

    def add_sub(self, list):
        for i, s in enumerate(list):
            list[i] = "sub-" + s
        return list

    def save_stats(self, stats_filename, _type):
        stat_df_paths = self.__extract_path(stats_filename)

        if stat_df_paths:
            print("stats file found for " + str(len(stat_df_paths)) + " subjects")
            if _type == 0:
                # stats_aseg(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.stats_aseg(stat_df_paths)
            elif _type == 1:
                # stats_aparcDTK(stat_df_paths).to_csv(SAVE_PATH + save_filename, index=False)
                return self.stats_aparcDTK(stat_df_paths)
        else:
            print("no file found")

    def stats_aseg(self, subj_paths):
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

    def stats_aparcDTK(self, subj_paths):
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

    def free_stats_aseg(self, subj_paths):
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

    def free_stats_aparcDTK(self, subj_paths):
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

    def save_stats(self, which=(True, True, True), names=("aseg.csv", "aseg_right.csv", "aseg_left.csv")):

        if not os.path.exists(self.data_path + "/" + self.name):
            os.makedirs(self.data_path + self.name)

        if which[0]:
            self.df_stats_aseg.to_csv(self.data_path + "/" + self.name + "/" + names[0])
        if which[1]:
            self.df_stats_aparkL.to_csv(self.data_path + "/" + self.name + "/" + names[1])
        if which[2]:
            self.df_stats_aparkR.to_csv(self.data_path + "/" + self.name + "/" + names[2])

    def __extract_path(self, filename, data_path):
        # set of all the subjects for easier computation
        subj_list_numbers = set(self.subj_list)

        # creates a list with all the subjects that are in the list
        # for s in subj_list:
        #     if len(s.split("/")) > 4:
        #         subj_list_numbers.add(s.split("/")[-4])
        # print(subj_list_numbers)

        paths_found = []
        for path, subdirs, files in os.walk(data_path):
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

    def __init__(self, stat_df_1, stat_df_2, name, alpha, base_path, columns_to_test=None, max_plot=500):
        """

        :param stat_df_1:
        :param stat_df_2:
        :param name:
        :param alpha:
        :param base_path:
        :param columns_to_test:
        :param max_plot:
        """
        if isinstance(stat_df_1, Stats):
            self.stat_df_1 = stat_df_1
        if isinstance(stat_df_2, Stats):
            self.stat_df_2 = stat_df_2
        else:
            raise ("stats of the wrong class")
        self.base_path = base_path

        self.data_path = self.base_path + "/data"
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.subjects_list = self.df["ID"].tolist()
        self.columns_list = self.df.columns.tolist()

        self.name = name
        self.alpha = alpha
        self.max_plot = max_plot

        self.stat_df_result = None
        self.stat_test(columns_to_test)


    def violin(self, columns=None, n_subplots=10, n_rows=2):
        plots = 0

        _df1 = self.stat_df_1
        _df2 = self.stat_df_2

        if not columns:
            columns = _df1.columns
            columns = columns.intersection(_df2.columns).tolist()
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
                            self.data_path + "/images/img_violin_" + self.name + " - " + stats_2.name + "_" + str(
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

                self.__violin_plot(axs[plots % n_subplots], a, b)
                plots += 1

            if plots >= self.max_plot:  # to avoid plotting too much
                break

    def bland_altmann(self, columns=None, n_subplots=4, n_rows=2):
        plots = 0

        _df1 = self.stat_df_1
        _df2 = self.stat_df_2
        if not columns:
            columns = _df1.columns
            columns = columns.intersection(_df2.columns).tolist()
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
                        fig.savefig(self.data_path + "/images/img_ba_" + self.name + " - " + stats_2.name + "_" + str(
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
                self.__bland_altman_plot(axs[plots % n_subplots], a, b)
                plots += 1

            if plots >= 20:  # to avoid plotting too much
                break

    def stat_test(self, columns):
        # input: query, df1 name, df2 name, subj_table, list of all test results
        _df1 = self.stat_df_1
        _df2 = self.stat_df_2
        r_all = []

        # se non viene dato un input fa il test per tutte le colonne
        if not columns:
            columns = _df1_filtered.columns
            columns.intersection(_df2_filtered.columns).tolist()
        # if not columns:
        #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     columns = range(2, max_len)

        for column_to_compare in columns:
            a = pd.to_numeric(_df1_filtered.loc[:, column_to_compare], errors='coerce')
            b = pd.to_numeric(_df2_filtered.loc[:, column_to_compare], errors='coerce')
            # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):

                r1, p1, o1 = __mann_whitney(a, b)
                r2, p2, o2 = __t_test(a, b)
                d, rd = __cohens_d(a, b)

                if isinstance(column_to_compare, int):
                    column_to_compare_name = _df1_filtered.columns[column_to_compare]

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
                print(f"no data in category {column_to_compare}")
            self.__save_dataframe(r_all)

    def bonferroni_correction(self, save=False):
        updated_ST = self.bonferroni_correction_param()
        print(updated_ST)
        for i, row in self.stat_df_result.iterrows():
            if row[1] < updated_ST:
                row[3] = f"p-value: {row[0]} - null hypothesis rejected, means are not statistically equal"
                row[2] = 1
            if row[4] < updated_ST:
                row[6] = f"p-value: {row[3]} - null hypothesis rejected, the datasets have a different distribution"
                row[5] = 1
            row.loc["significance_threshold_used"] = updated_ST
            df.iloc[i, :] = row
            if save == True:
                df.to_csv(self.data_path + f"{query}_bonferroni_corrected.csv")

    def save_data(self, filename):

        """
        to csv in basepath + filename
        :param filename:
        :return:
        """
        self.stat_df_result.to_csv(self.base_path + filename)

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
        df = pd.DataFrame()

        for item in list_to_save:
            self.stat_df_result = pd.concat([df, pd.DataFrame({"mann_whitney p_value": item["mann_whitney"]["p_value"],
                                                               "mann_whitney outcome": item["mann_whitney"]["outcome"],
                                                               "mann_whitney message": item["mann_whitney"]["result"],
                                                               "t_test p_value": item["t_test"]["p_value"],
                                                               "t_test outcome": item["t_test"]["outcome"],
                                                               "t_test message": item["t_test"]["result"],
                                                               "cohens d value": item["d"]["d_value"],
                                                               "cohens d result": item["d"]["result"],
                                                               "significance_threshold_used": self.alpha
                                                               }, index=[item["name"]])])

        # df.to_csv(self.base_path + _name)  # , index=False

    def __cohens_d(self, _a, _b):
        n1, n2 = len(a), len(b)
        var1, var2 = np.var(a, ddof=1), np.var(b, ddof=1)

        SDpooled = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        d = (np.mean(a) - np.mean(b)) / SDpooled

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
        sns.violinplot(ax=ax, data=df, hue="Group", x="Area", y="Data", split=True)
        ax.title.set_text(_a.name + "\n" + queries[0].split("=")[-1])
        # ax.yaxis.set_major_formatter(plt.FormatStrFormatter('{:.3g}'))
        ax.set_xlabel("")

    def __bland_altman_plot(self, _ax, _a, _b):
        # Compute mean and difference between two series
        mean = np.mean([_a, _b], axis=0)
        diff = _a - _b

        # Compute mean difference and standard deviation of difference
        md = np.mean(diff)
        sd = np.std(diff, axis=0)

        # Create plot
        ax.scatter(mean, diff, s=10)
        ax.axhline(md, color='gray', linestyle='--')
        ax.axhline(md + 1.96 * sd, color='gray', linestyle='--')
        ax.axhline(md - 1.96 * sd, color='gray', linestyle='--')
        ax.set_xlabel('Mean')
        ax.set_ylabel('Difference')
        ax.set_title(_a.name + "\n" + queries[0].split("=")[-1])
        ax.legend(['Mean difference', '95% limits of agreement'])

    def __get_column(self, column_to_compare):
        if isinstance(column_to_compare, int):
            a = df1.iloc[:, column_to_compare]
            b = df2.iloc[:, column_to_compare]

        if isinstance(column_to_compare, str):
            a = df1.loc[:, column_to_compare]
            b = df2.loc[:, column_to_compare]

        return a, b

    def __correction_param(self):
        return self.alpha / len(self.stat_df_result)
