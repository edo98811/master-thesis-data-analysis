import pandas as pd
import matplotlib.pyplot as plt
import os
import re
from scipy import stats
import scipy as sp
import seaborn as sns
import data_manipulation as dm
import numpy as np
from copy import deepcopy
import pingouin as pg
import FastsurferTesting_pc as ft
from sklearn import metrics
from sklearn.linear_model import LinearRegression, HuberRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score

"""
todo:
- cambiare nome var subj list in table
- controllare global plots_n n in stats+
- mettere un underscore in metodi privati



- aggiungere statistiche a line plot
- provare wilcoxon test
- salvare statistiche su linee saltate eccetera
- plot del pvalue per area
- ADNI e cose per ospedali portoghesi

"""

"""
for table in self.df_list_obj:
    self.subj_lists.append(table.subj_list) # usare statistiche
    # non posso creare la variabile per le colonne perchè sono diverse per i tre dataframes 
    
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

ATTRIBUTES TABLE

        self.df = df_subj

        self.subjects_list = self.df["ID"].tolist() (NOT FILTERED) 

        self.processed_path = p_path
        self.base_path = b_path
        self.data_path = b_path + d_folder
        self.name = name

ATTRIBUTES SUMMARY

        self.df_list_obj = stats_df_list

        self.base_path = b_path
        self.data_path = self.base_path + d_folder

        # self.subjects_list = self.df["ID"].tolist()
        # self.columns_list = self.df.columns.tolist()

        self.name = name
        self.max_plot = max_plot
        # self.columns_list =

        global plots_n
        plots_n = 0
        
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
        if not os.path.exists(self.data_path + "images\\"):
            os.makedirs(self.data_path + "images\\")

        # create the common
        # self.subjects_list = set(stats_df_2.add_sub(list(self.subjects_list)))

        # other important variables
        self.name = name
        self.alpha = alpha
        self.updated_alpha = "no correction"
        self.max_plot = max_plot

        self.stat_df_result = None
        global plots_n
        plots_n = 0
    ATTRIBUTES COMPARISON
    
            self.stat_df_1 = stats_df_1
            self.stat_df_2 = stats_df_2


        self.base_path = b_path
        self.data_path = self.base_path + d_folder

        # create common subjects list and common column list
        self.subjects_list = set(self.stat_df_1.df_subj["ID"].tolist()).intersection(
            set(self.stat_df_2.df_subj["ID"].tolist()))
        self.columns_list = set(self.stat_df_1.df_subj.columns.tolist()).intersection(
            set(self.stat_df_2.df_subj.columns.tolist()))

        # self.subjects_list = set(stats_df_2.add_sub(list(self.subjects_list)))

        self.name = name
        self.alpha = alpha
        self.updated_alpha = "no correction"
        self.max_plot = max_plot

        self.stat_df_result = None
        
        global plots_n
 
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


"""


entities 
    list of Stat objects
     

"""


class SummaryPlot_updated:
    def __init__(self, name, b_path, stats_df_list, d_folder="data_testing_ADNI\\", max_plot=500):
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
        # if not os.path.exists(self.data_path + "\\images"):
        #     os.makedirs(self.data_path + "\\images")
        #     os.makedirs(self.data_path + "\\images_linear_regression")
        #     os.makedirs(self.data_path + "\\images_huber")

        # self.subjects_list = self.df["ID"].tolist()
        # self.columns_list = self.df.columns.tolist()

        self.name = name
        self.max_plot = max_plot
        # self.columns_list =

        global plots_n
        plots_n = 0

    # in teoria dovrei filtrarla prima
    def comparison_plot(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=("ID"), n_subplots=4, n_rows=2):
        """
        :param c_to_exclude:
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        raise "old"
        #
        # df_list = []
        # subj_lists = []
        # # saves the dataframes from the stats object
        # LogWriter.log(f"\n")
        # LogWriter.log(f"    scatter plot:{self.name}...")
        # for d in data:
        #     if d == "aseg":
        #         for table in self.df_list_obj:
        #             df_list.append(table.df_stats_aseg)
        #             subj_lists.append(table.df_stats_aseg["ID"].tolist())
        #     elif d == "aparcR":
        #         for table in self.df_list_obj:
        #             df_list.append(table.df_stats_aparcL)
        #             subj_lists.append(table.df_stats_aparcL["ID"].tolist())
        #     elif d == "aparcL":
        #         for table in self.df_list_obj:
        #             df_list.append(table.df_stats_aparcR)  # table
        #             subj_lists.append(table.df_stats_aparcR["ID"].tolist())
        #
        #     # creates the age series, to move up
        #     ages = []
        #     legend = []
        #     for table, subj_list in zip(self.df_list_obj, subj_lists):
        #         s = list(ft.Stats.delete_sub(subj_list))
        #         t = table.df_subj[table.df_subj['ID'].isin(s)]
        #         a = t.loc[:, "age"].tolist()
        #         ages.append(pd.to_numeric(a, errors='coerce'))
        #         # legend.append(table.name)
        #     del a, t, s
        #     columns = df_list[0].columns
        #     # columns = columns.intersection(_df2.columns).tolist()
        #     # if not columns:
        #     #     max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        #     #     columns = range(2, max_len)
        #     not_done = []
        #     for column_to_compare in columns:
        #         if column_to_compare not in c_to_exclude:
        #             title = f"{d} {column_to_compare}"
        #             serieses = []
        #             # selects the column from all the dataframes and puts them in a list of series
        #             for i, df in enumerate(df_list):
        #                 series = pd.to_numeric(df[column_to_compare], errors='coerce')
        #                 series.rename(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
        #                 legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")
        #                 LogWriter.log(f"        {d}_{self.df_list_obj[i].name}_{column_to_compare}. "
        #                               f"series name {series.name}")
        #
        #                 if series.any() and series.notnull().all():
        #                     serieses.append(series)
        #
        #                 else:
        #                     # print(series)
        #                     LogWriter.log(f"        comparison not possible for column {column_to_compare}")
        #                     not_done.append(column_to_compare)
        #                     break
        #             if not len(serieses):
        #                 continue
        #
        #             # a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
        #             # if it needs to create a new figure it creates it
        #             if not plots_n % n_subplots:
        #                 if plots_n > 1:
        #                     fig.savefig(f"{self.data_path}images\\img_{d}_scatter_{self.name}"
        #                                 f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
        #                     # plt.close(fig)  # close the figure window
        #                     # handles, labels = axs[1].get_legend_handles_labels()
        #                     # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
        #                 fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
        #                 axs = axs.ravel()
        #                 plt.subplots_adjust(hspace=0.5)
        #                 plt.subplots_adjust(wspace=0.2)
        #                 # mng = plt.get_current_fig_manager()
        #                 # mng.full_screen_toggle()
        #
        #             # print(plots_n % N_SUBPLOTS)
        #
        #             """
        #             now i have two series
        #             serieses: series of data
        #             ages: series of ages
        #
        #             i can do the scatter plots_n of this
        #             """
        #             index = plots_n % n_subplots
        #             # print(index)
        #             self.__scatter_plot(axs[index], serieses, ages, title, legend)
        #             plots_n += 1
        #
        #             if plots_n >= self.max_plot:  # to avoid plotting too much
        #                 break
        #
        #     if plots_n % n_subplots != 0:
        #         fig.savefig(f"{self.data_path}images\\img_{d}_scatter_{self.name}"
        #                     f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
        # del axs, fig
        #
        # LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
        # not_done_str = ' | '.join(not_done)
        # LogWriter.log(f"    skipped: {not_done_str}")
        # # fig.savefig(
        # #     self.data_path + "images\\img_{data_scatter_" + self.name + " - " + self.name + "_" + str(
        # #         plots_n) + ".png")  # save the figure to file
        # """
        # idea
        #     plot con 4
        #     all'inizio tutti i puntini, ognuno con un colore diverso in base alla serie da cui proviene
        #     poi provo a far la linea
        # """

    def create_list(self, d):
        df_list = []
        subj_lists = []
        columns = []
        if d == "aseg":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aseg)
                subj_lists.append(table.df_stats_aseg["ID"].tolist())
                columns.append(set(table.df_stats_aseg.columns.tolist()))
        elif d == "aparcR":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aparcL)
                subj_lists.append(table.df_stats_aparcL["ID"].tolist())
                columns.append(set(table.df_stats_aparcL.columns.tolist()))
        elif d == "aparcL":
            for table in self.df_list_obj:
                df_list.append(table.df_stats_aparcR)
                subj_lists.append(table.df_stats_aparcR["ID"].tolist())
                columns.append(set(table.df_stats_aparcR.columns.tolist()))

        columns_set = set(columns[0])
        for column in columns[1:]:
            columns_set.intersection(set(column))

        return df_list, subj_lists, columns_set

    @staticmethod
    def create_plot(n_subplots, n_rows):

        fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
        axs = axs.ravel()
        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.2)

        return fig, axs

    @staticmethod
    def data_points_calculation(table, subj_list, df_element, data_points_list):

        s = list(ft.Stats.delete_sub(subj_list))
        t = table.df_subj[table.df_subj['ID'].isin(s)]
        ages = t.loc[:, "age"]
        ages.index = subj_list

        full_table = pd.concat([df_element, ages], axis=1)
        age_groups = np.arange(55, 90, 5)

        # Create a new DataFrame to store the results
        # full_table.drop(columns="Unnamed: 0", inplace=True)
        full_table['AgeGroup'] = pd.cut(full_table['age'], bins=age_groups, labels=age_groups[:-1])
        data_points = full_table.groupby('AgeGroup').mean()
        data_std = full_table.groupby('AgeGroup').std()
        data_n = full_table.groupby('AgeGroup').count().iloc[:, 0]

        # concatenate the dataframes, adding keys for each dataframe
        data_table_all_info = pd.concat([data_points, data_std, data_n], axis=1, keys=['value', 'std', 'count'])

        # create a multi-index from the column names and the dataframe keys
        list_indexes = [(col, key) for key in ['value', 'std'] for col in data_points.columns]
        list_indexes.append(("count", "count"))
        columns = pd.MultiIndex.from_tuples(list_indexes)
        data_table_all_info.columns = columns

        data_table_all_info.index = [f"{age_groups[i]} - {age_groups[i + 1]}" for i in range(len(age_groups) - 1)]

        # print(data_points.head())
        data_points_list.append(data_table_all_info)

    def series_and_legend(self, data_points_list, column_to_compare, d, not_done):
        serieses = []
        legend = []

        for i, df in enumerate(data_points_list):

            # creation of the serieses to plot and ages
            # series = pd.to_numeric(df[column_to_compare, "value"], errors='coerce')
            if (column_to_compare, "std") in df.columns.tolist():
                series = df.loc[:, (column_to_compare, ["value", "std"])]
            else:
                LogWriter.log(f"        not possible: column{column_to_compare}")
                not_done.append(column_to_compare)

            series.name = f"{d}_{self.df_list_obj[i].name}_{column_to_compare}"
            legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")

            # to add
            for i, k in enumerate(series[(column_to_compare, "value")]):
                if k == "nan":
                    series.iloc[i] = 0
                    pass

            serieses.append(series)

        return serieses, legend

    def _model_fit_legend(self, data_points_list, column_to_compare, d, not_done):
        serieses = []
        legend = []

        for i, df in enumerate(data_points_list):

            # creation of the serieses to plot and ages
            # series = pd.to_numeric(df[column_to_compare, "value"], errors='coerce')
            if column_to_compare in df.columns.tolist():
                series = df.loc[:, [column_to_compare, "age"]]
            else:
                LogWriter.log(f"        not possible: column{column_to_compare}")
                not_done.append(column_to_compare)

            series.name = f"{d}_{self.df_list_obj[i].name}_{column_to_compare}"
            legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")

            # to add
            # for i, k in enumerate(series[(column_to_compare, "value")]):
            #     if k == "nan":
            #         series.iloc[i] = 0
            #         pass

            serieses.append(series)

        return serieses, legend
    def _model_fit_legend_mmse(self, data_points_list, column_to_compare, d, not_done):
        serieses = []
        legend = []

        for i, df in enumerate(data_points_list):

            # creation of the serieses to plot and ages
            # series = pd.to_numeric(df[column_to_compare, "value"], errors='coerce')
            if column_to_compare in df.columns.tolist():
                series = df.loc[:, [column_to_compare, "MMSE"]]
            else:
                LogWriter.log(f"        not possible: column{column_to_compare}")
                not_done.append(column_to_compare)

            series.name = f"{d}_{self.df_list_obj[i].name}_{column_to_compare}"
            legend.append(f"{d}_{self.df_list_obj[i].name}_{column_to_compare}")

            # to add
            # for i, k in enumerate(series[(column_to_compare, "value")]):
            #     if k == "nan":
            #         series.iloc[i] = 0
            #         pass

            serieses.append(series)

        return serieses, legend

    def comparison_plot_line(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=("ID", "Unnamed: 0"), c_to_keep=None,
                             n_subplots=4,
                             n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    scatter plot with ages: {self.name}...")

        for d in data:
            df_list, subj_lists, columns = self.create_list(
                d)  # questa si potrebbe fare anche in init, cosi lo devo fare una volta sola
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for table, subj_list, df_element in zip(self.df_list_obj, subj_lists, df_list):
                df_element = df_element.set_index("ID")  # to do in init o in table creation in stats
                df_element.drop(["Unnamed: 0"], axis=1, inplace=True)  # da controllare
                self.data_points_calculation(table, subj_list, df_element, data_points_list)

                # aggiungere metodo per calcolare devstd

                # idea: copiare cme ho fatto su comparisons

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self.series_and_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__line_plot(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                            f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")

    def scatter_plot(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=("ID", "Unnamed: 0"), c_to_keep=None,
                     n_subplots=4,
                     n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    line plot:{self.name}...")

        for d in data:
            df_list, subj_lists, columns = self.create_list(
                d)  # questa si potrebbe fare anche in init, cosi lo devo fare una volta sola
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for table, subj_list, df_element in zip(self.df_list_obj, subj_lists, df_list):
                df_element = df_element.set_index("ID")  # to do in init o in table creation in stats
                df_element.drop(["Unnamed: 0"], axis=1, inplace=True)  # da controllare

                s = list(ft.Stats.delete_sub(subj_list))
                t = table.df_subj[table.df_subj['ID'].isin(s)]
                ages = t.loc[:, "age"]
                ages.index = subj_list
                full_table = pd.concat([df_element, ages], axis=1)
                # self.data_points_calculation(table, subj_list, df_element, data_points_list)
                data_points_list.append(full_table)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__scatter_plot2(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")

    def scatter_plot_aseg_normalized_linear_regression(self, data=("aseg_normalized",), c_to_exclude=(), c_to_keep=None,
                                                       n_subplots=6,
                                                       n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        if not os.path.exists(self.data_path + "\\images_linear_regression"):
            os.makedirs(self.data_path + "\\images_linear_regression")
        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    scatter plot with ages: {self.name}...")
        if hasattr(self, 'fitted_models'): del self.fitted_models
        self.fitted_models = {
            "legend_entry": [],
            "first_coefficient": [],
            "intercept": [],
            "R2": [],
            "message": []}

        for d in data:
            df_list = [n.aseg_normalized for n in self.df_list_obj]
            columns = df_list[0].columns  # da mettere a posto magari
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for df_element in df_list:
                data_points_list.append(df_element)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(
                                f"{self.data_path}images_linear_regression\\img_{d}_scatter_normalized{self.name}"
                                f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__scatter_plot_linear_regression(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images_linear_regression\\img_{d}_scatter_normalized{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")
            pd.DataFrame.from_dict(self.fitted_models).to_excel(f"{self.data_path}\\{self.name}_{d}_linear.xlsx")
            # dm.write_txt(self.fitted_models, f"{self.data_path}\\{self.name}_{d}.txt")
    def scatter_plot_aseg_mmse(self, data=("aseg_normalized_mmse",), c_to_exclude=(), c_to_keep=None,
                                                      n_subplots=6,
                                                      n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        if not os.path.exists(self.data_path + "\\images_confidence_intervals"):
            os.makedirs(self.data_path + "\\images_confidence_intervals")

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    scatter plot with ages: {self.name}...")
        if hasattr(self, 'fitted_models'): del self.fitted_models
        self.fitted_models = {
            "legend_entry": [],
            "first_coefficient": [],
            "intercept": [],
            "R2": []}

        for d in data:
            if data == "aseg_normalized":
                df_list = [n.aseg_normalized for n in self.df_list_obj]
            elif data == "aseg_normalized_mmse":
                df_list = [n.aseg_normalized_mmse for n in self.df_list_obj]
            columns = df_list[0].columns  # da mettere a posto magari
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for df_element in df_list:
                data_points_list.append(df_element)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images\\img_{d}_confidence_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__scatter_plot_confidence_intervals_internet(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images\\img_{d}_confidence_{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")
            pd.DataFrame.from_dict(self.fitted_models).to_excel(f"{self.data_path}\\{self.name}_{d}_linear.xlsx")
            # dm.write_txt(self.fitted_models, f"{self.data_path}\\{self.name}_{d}.txt")
    def scatter_plot_aseg_normalized_regression_confidence(self, data=("aseg_normalized",), c_to_exclude=(), c_to_keep=None,
                                                      n_subplots=6,
                                                      n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        if not os.path.exists(self.data_path + "\\images_confidence_intervals"):
            os.makedirs(self.data_path + "\\images_confidence_intervals")

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    scatter plot with ages: {self.name}...")
        if hasattr(self, 'fitted_models'): del self.fitted_models
        self.fitted_models = {
            "legend_entry": [],
            "first_coefficient": [],
            "intercept": [],
            "R2": []}

        for d in data:
            df_list = [n.aseg_normalized for n in self.df_list_obj]
            columns = df_list[0].columns  # da mettere a posto magari
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for df_element in df_list:
                data_points_list.append(df_element)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images_confidence_intervals\\img_{d}_confidence_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__scatter_plot_confidence_intervals_internet(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images_confidence_intervals\\img_{d}_confidence_{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")
            pd.DataFrame.from_dict(self.fitted_models).to_excel(f"{self.data_path}\\{self.name}_{d}_linear.xlsx")
            # dm.write_txt(self.fitted_models, f"{self.data_path}\\{self.name}_{d}.txt")
    def scatter_plot_aseg_normalized_huber_regression(self, data=("aseg_normalized",), c_to_exclude=(), c_to_keep=None,
                                                      n_subplots=6,
                                                      n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """
        if not os.path.exists(self.data_path + "\\images_huber_loss"):
            os.makedirs(self.data_path + "\\images_huber_loss")
        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    scatter plot with ages: {self.name}...")
        if hasattr(self, 'fitted_models'): del self.fitted_models
        self.fitted_models = {
            "legend_entry": [],
            "first_coefficient": [],
            "intercept": [],
            "R2": [],
            "message": []}

        for d in data:
            df_list = [n.aseg_normalized for n in self.df_list_obj]
            columns = df_list[0].columns  # da mettere a posto magari
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for df_element in df_list:
                data_points_list.append(df_element)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images_huber_loss\\img_{d}_scatter_normalized_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__scatter_plot_huber(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images_huber_loss\\img_{d}_scatter_normalized_{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")
            pd.DataFrame.from_dict(self.fitted_models).to_excel(f"{self.data_path}\\{self.name}_{d}_huber.xlsx")
            # dm.write_txt(self.fitted_models, f"{self.data_path}\\{self.name}_{d}.txt")

    def model_fit(self, data=("aseg", "aparcL", "aparcR"), c_to_exclude=("ID", "Unnamed: 0"), c_to_keep=None,
                  n_subplots=4,
                  n_rows=2):
        """
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :param n_subplots:
        :param n_rows:
        :return:
        """

        # saves the dataframes from the stats object
        LogWriter.log(f"\n")
        LogWriter.log(f"    line plot:{self.name}...")

        for d in data:
            df_list, subj_lists, columns = self.create_list(
                d)  # questa si potrebbe fare anche in init, cosi lo devo fare una volta sola
            plots_n = 0

            if c_to_keep is not None:
                columns = [x for x in columns if x in c_to_keep]

            not_done = []
            data_points_list = []

            for table, subj_list, df_element in zip(self.df_list_obj, subj_lists, df_list):
                df_element = df_element.set_index("ID")  # to do in init o in table creation in stats
                df_element.drop(["Unnamed: 0"], axis=1, inplace=True)  # da controllare

                s = list(ft.Stats.delete_sub(subj_list))
                t = table.df_subj[table.df_subj['ID'].isin(s)]
                ages = t.loc[:, "age"]
                ages.index = subj_list
                full_table = pd.concat([df_element, ages], axis=1)
                # self.data_points_calculation(table, subj_list, df_element, data_points_list)
                data_points_list.append(full_table)

            for column_to_compare in columns:
                if column_to_compare not in c_to_exclude:
                    # LogWriter.log(f"        column{column_to_compare}")

                    title = f"{d} {column_to_compare} \n {self.name}"

                    serieses, legend = self._model_fit_legend(data_points_list, column_to_compare, d, not_done)

                    if not len(serieses):
                        continue
                    # selects the column from all the dataframes and puts them in a list of series

                    if not plots_n % n_subplots:
                        if plots_n > 1:
                            fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                                        f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file
                        fig, axs = self.create_plot(n_subplots, n_rows)

                    self.__model_fit(axs[plots_n % n_subplots], serieses, title, legend)
                    plots_n += 1

                    if plots_n >= self.max_plot:  # to avoid plotting too much
                        break

            if plots_n % n_subplots != 0 or (plots_n % n_subplots == 0 and plots_n <= n_subplots):
                fig.savefig(f"{self.data_path}images\\img_{d}_line_{self.name}"
                            f"_{str(plots_n - plots_n % n_subplots)}-{str(plots_n)}.png")  # save the figure to file
            del axs, fig

            LogWriter.log(f"    plotted {plots_n} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
            LogWriter.log(f"    skipped: {not_done_str}")

    @staticmethod
    def __scatter_plot(ax, data, ages, title, legend):
        max_ = 0
        for series, age, legend_entry in zip(data, ages, legend):
            ax.scatter(age, series.tolist(), label=legend_entry)  # mettere il nome della serie e le cose qui
            LogWriter.log(f"        {series.name}")
            if series.max() > max_:
                max_ = series.max()

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    @staticmethod
    def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None, color="b"):
        """Return an axes of confidence bands using a simple approach.

        Notes
        -----
        .. math:: \left| \: \hat{\mu}_{y|x0} - \mu_{y|x0} \: \right| \; \leq \; T_{n-2}^{.975} \; \hat{\sigma} \; \sqrt{\frac{1}{n}+\frac{(x_0-\bar{x})^2}{\sum_{i=1}^n{(x_i-\bar{x})^2}}}
        .. math:: \hat{\sigma} = \sqrt{\sum_{i=1}^n{\frac{(y_i-\hat{y})^2}{n-2}}}

        References
        ----------
        .. [1] M. Duarte.  "Curve fitting," Jupyter Notebook.
           http://nbviewer.ipython.org/github/demotu/BMC/blob/master/notebooks/CurveFitting.ipynb

        """
        if ax is None:
            ax = plt.gca()

        ci = t * s_err * np.sqrt(1 / n + (x2 - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
        ax.fill_between(x2, y2 + ci, y2 - ci, alpha=0.3, color=color)

        return ax

    @staticmethod
    def plot_ci_bootstrap(xs, ys, resid, nboot=500, ax=None, color=None):
        """Return an axes of confidence bands using a bootstrap approach.

        Notes
        -----
        The bootstrap approach iteratively resampling residuals.
        It plots `nboot` number of straight lines and outlines the shape of a band.
        The density of overlapping lines indicates improved confidence.

        Returns
        -------
        ax : axes
            - Cluster of lines
            - Upper and Lower bounds (high and low) (optional)  Note: sensitive to outliers

        References
        ----------
        .. [1] J. Stults. "Visualizing Confidence Intervals", Various Consequences.
           http://www.variousconsequences.com/2010/02/visualizing-confidence-intervals.html

        """
        if ax is None:
            ax = plt.gca()

        bootindex = sp.random.randint

        for _ in range(nboot):
            resamp_resid = resid[bootindex(0, len(resid) - 1, len(resid))]
            # Make coeffs of for polys
            pc = sp.polyfit(xs, ys + resamp_resid, 1)
            # Plot bootstrap cluster
            ax.plot(xs, sp.polyval(pc, xs), "b-", linewidth=2, alpha=3.0 / float(nboot))

        return ax

    def __scatter_plot_confidence_intervals_internet(self, ax, data, title, legend):
        max_ = 0
        LogWriter.log(f"    regression with intervals from normalized data {' | '.join(legend)} ")

        for i, (series, legend_entry) in enumerate(zip(data, legend)):
            color = next(ax._get_lines.prop_cycler)['color']
            y = pd.to_numeric(series.iloc[:, 0], errors='coerce')
            x = pd.to_numeric(series.iloc[:, 1], errors='coerce')
            if max(y) > max_: max_ = max(y) * 1.5
            p, cov = np.polyfit(x, y, 1, cov=True)  # parameters and covariance from of the fit of 1-D polynom.
            y_model = np.polyval(p, x)  # model using the fit parameters; NOTE: parameters here are coefficients

            # Statistics
            n = x.size  # number of observations
            m = p.size  # number of parameters
            dof = n - m  # degrees of freedom
            t = stats.t.ppf(0.975, n - m)  # t-statistic; used for CI and PI bands

            # Estimates of Error in Data/Model
            resid = y - y_model  # residuals; diff. actual data from predicted values
            chi2 = np.sum((resid / y_model) ** 2)  # chi-squared; estimates error in data
            chi2_red = chi2 / dof  # reduced chi-squared; measures goodness of fit
            s_err = np.sqrt(np.sum(resid ** 2) / dof)  # standard deviation of the error
            R2 = r2_score(x, y_model)

            self.fitted_models["legend_entry"].append(legend_entry)
            self.fitted_models["first_coefficient"].append(p[0])
            self.fitted_models["intercept"].append(p[1])
            self.fitted_models["R2"].append(R2)


            # Data
            ax.plot(x, y, "o", alpha=0.5, label=legend_entry, color=color)
                # , color="#b9cfe7", markersize=8,
                # markeredgewidth=1, markeredgecolor="b", markerfacecolor="None")

            # Fit
            ax.plot(x, y_model, "-", color=color, alpha = 0.3)

            #, color="0.1", linewidth=1.5, alpha=0.5, label="Fit")
            x2 = np.linspace(np.min(x), np.max(x), 100)
            y2 = np.polyval(p, x2)

            # Confidence Interval (select one)
            SummaryPlot_updated.plot_ci_manual(t, s_err, n, x, x2, y2, ax=ax, color=color)
            # plot_ci_bootstrap(x, y, resid, ax=ax)

            # Prediction Interval
            pi = t * s_err * np.sqrt(1 + 1 / n + (x2 - np.mean(x)) ** 2 / np.sum((x - np.mean(x)) ** 2))
            ax.fill_between(x2, y2 + pi, y2 - pi, color="None", linestyle="--", alpha=0.5)
            ax.plot(x2, y2 - pi, "--", color="0.5", label="_95% Prediction Limits")
            ax.plot(x2, y2 + pi, "--", color="0.5")

        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    def __scatter_plot_huber(self, ax, data, title, legend):
        max_ = 0
        LogWriter.log(f"    huber regression from normalized data {' | '.join(legend)} ")
        for i, (series, legend_entry) in enumerate(zip(data, legend)):

            values = pd.to_numeric(series.iloc[:, 0], errors='coerce')
            age = pd.to_numeric(series.iloc[:, 1], errors='coerce')
            max_ = max(values) * 1.5
            ax.scatter(age, values.tolist(), label=legend_entry)  # mettere il nome della serie e le cose qui

            x = np.linspace(min(age), max(age), 100)


            huber_loss_model = HuberRegressor().fit(np.array(age).reshape(-1, 1),
                                                    np.array(values).reshape(-1, 1).ravel())
            # r2.append(r2_score(linear_model.predict(avg.reshape(-1,1), values).reshape(-1,1)
            results = huber_loss_model.predict(x.reshape(-1, 1))

            if series.index.tolist():
                ax.plot(x, results,
                        label="_legend_entry")

            R2 = r2_score(np.array(values).reshape(-1, 1), huber_loss_model.predict(np.array(age).reshape(-1, 1)))

            self.fitted_models["legend_entry"].append(legend_entry)
            self.fitted_models["first_coefficient"].append(huber_loss_model.coef_[0])
            self.fitted_models["intercept"].append(huber_loss_model.intercept_)
            self.fitted_models["R2"].append(R2)
            self.fitted_models["message"].append(
                f"{legend_entry} equation: {huber_loss_model.coef_[0]}x + {huber_loss_model.intercept_}  r2: {R2}")

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    def __scatter_plot_linear_regression(self, ax, data, title, legend):
        max_ = 0

        for i, (series, legend_entry) in enumerate(zip(data, legend)):

            values = pd.to_numeric(series.iloc[:, 0], errors='coerce')
            age = pd.to_numeric(series.iloc[:, 1], errors='coerce')
            max_ = max(values) * 1.5
            ax.scatter(age, values.tolist(), label=legend_entry)  # mettere il nome della serie e le cose qui

            x = np.linspace(min(age), max(age), 100)

            LogWriter.log(f"    linear regression from normalized data {' | '.join(legend)} ")
            linear_model = LinearRegression().fit(np.array(age).reshape(-1, 1), np.array(values).reshape(-1, 1))
            # r2.append(r2_score(linear_model.predict(avg.reshape(-1,1), values).reshape(-1,1)
            results = linear_model.predict(x.reshape(-1, 1))

            if series.index.tolist():
                ax.plot(x, results,
                        label="_legend_entry")

            R2 = r2_score(np.array(values).reshape(-1, 1), linear_model.predict(np.array(age).reshape(-1, 1)))

            self.fitted_models["legend_entry"].append(legend_entry)
            self.fitted_models["first_coefficient"].append(linear_model.coef_[0][0])
            self.fitted_models["intercept"].append(linear_model.intercept_[0])
            self.fitted_models["R2"].append(R2)
            self.fitted_models["message"].append(
                f"{legend_entry} equation: {linear_model.coef_[0][0]}x + {linear_model.intercept_[0]}  r2: {R2}")

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    @staticmethod
    def __line_plot(ax, data, title, legend):
        max_ = 0

        for series, legend_entry in zip(data, legend):
            # series = series.reset_index(level=[1], drop=True)
            confidence_up = series.iloc[:, 0] + 2 * series.iloc[:, 1]
            confidence_down = series.iloc[:, 0] - 2 * series.iloc[:, 1]

            values = pd.to_numeric(series.iloc[:, 0], errors='coerce')
            # LogWriter.log(values)

            # values = series.iloc[:, 0]
            pattern = r"(\d+)\s*-\s*(\d+)"
            avg = []

            # x entries
            for index in values.index.tolist():

                match = re.match(pattern, index)
                if match:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))

                    avg.append(int((num1 + num2) / 2))

            LogWriter.log(f"    LINE PLOT {' | '.join(legend)} ")
            if series.index.tolist():
                ax.plot(avg, values.tolist(),
                        label=legend_entry)  # mettere il nome della serie e le cose qui
                ax.fill_between(avg, confidence_down, confidence_up, alpha=0.2)
                if confidence_up.max() > max_:
                    max_ = confidence_up.max()

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend()
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)

    @staticmethod
    def avg_vector(series, pattern=r"(\d+)\s*-\s*(\d+)"):

        avg = []

        # x entries
        for index in series.index.tolist():

            match = re.match(pattern, index)
            if match:
                num1 = int(match.group(1))
                num2 = int(match.group(2))

                avg.append(int((num1 + num2) / 2))
        return avg

    @staticmethod
    def __model_fit(ax, data, title, legend):

        max_ = 0

        for i, (series, legend_entry) in enumerate(zip(data, legend)):

            values = pd.to_numeric(series.iloc[:, 0], errors='coerce')
            ages = pd.to_numeric(series.iloc[:, 1], errors='coerce')
            max_ = max(values) * 1.5
            x = np.linspace(min(ages), max(ages), 100)

            LogWriter.log(f"    LINEAR REGRESSION {' | '.join(legend)} ")
            linear_model = LinearRegression().fit(np.array(ages).reshape(-1, 1), np.array(values).reshape(-1, 1))
            # r2.append(r2_score(linear_model.predict(avg.reshape(-1,1), values).reshape(-1,1)
            results = linear_model.predict(x.reshape(-1, 1))

            if series.index.tolist():
                ax.plot(x, results,
                        label=legend_entry)

            R21 = r2_score(linear_model.predict(np.array(ages).reshape(-1, 1)), np.array(values).reshape(-1, 1))

            LogWriter.log(f"    QUADRATIC LINEAR REGRESSION {' | '.join(legend)} ")
            quadratic_model = make_pipeline(PolynomialFeatures(2), LinearRegression())
            quadratic_model.fit(np.array(ages).reshape(-1, 1), np.array(values).reshape(-1, 1)).predict(
                (x.reshape(-1, 1)))

            results = quadratic_model.predict(x.reshape(-1, 1))

            if series.index.tolist():
                ax.plot(x, results,
                        label=legend_entry)

            R22 = r2_score(quadratic_model.predict(np.array(ages).reshape(-1, 1)), np.array(values).reshape(-1, 1))
            LogWriter.log(f"    CUBIC LINEAR REGRESSION {' | '.join(legend)} ")

            cubic_model = make_pipeline(PolynomialFeatures(2), LinearRegression())
            cubic_model.fit(np.array(ages).reshape(-1, 1), np.array(values).reshape(-1, 1)).predict((x.reshape(-1, 1)))
            results = cubic_model.predict(x.reshape(-1, 1))

            if series.index.tolist():
                ax.plot(x, results,
                        label=legend_entry)

            R23 = r2_score(cubic_model.predict(np.array(ages).reshape(-1, 1)), np.array(values).reshape(-1, 1))

            # print(f"R2 score {legend_entry}: {r2[-1]} ")

            textstr = '\n'.join((
                r'$R2 linear=%.2f$' % (R21,),
                r'$R2 quadratic=%.2f$' % (R22,),
                r'$R2 cubic=%.2f$' % (R23,)))

            ax.text(0.05 + 0.18 * i, 0.95, textstr, transform=ax.transAxes, fontsize=14,
                    verticalalignment='top')

        # Add a legend and axis labels
        ax.axis(ymin=0, ymax=max_)
        ax.legend(loc='lower right')
        ax.set_xlabel('Age')
        ax.set_ylabel('Data')
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
        ax.set_title(title)


class Comparison_updated:

    def __init__(self, name, b_path, stats_df_1, stats_df_2, alpha=0.05, d_folder="data_testing_ADNI/",
                 categories=("FastSurfer", "FreeSurfer"),
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
        if isinstance(stats_df_1, ft.Stats):
            self.stat_df_1 = stats_df_1
        else:
            raise "stats of the wrong class"
        if isinstance(stats_df_2, ft.Stats):
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
        # self.columns_list = set(self.stat_df_1.df_subj.columns.tolist()).intersection(
        #     set(self.stat_df_2.df_subj.columns.tolist()))

        # check that there are common subjects and define image path
        # if not self.subjects_list or not self.columns_list:
        #     raise "datasets do not have elements in common"

        if not os.path.exists(self.data_path + "images/"):
            os.makedirs(self.data_path + "images/")

        # create the common
        # self.subjects_list = set(stats_df_2.add_sub(list(self.subjects_list)))

        # other important variables
        self.name = name
        self.alpha = alpha
        self.updated_alpha = "no correction"
        self.max_plot = max_plot
        self.categories = categories

        self.stat_df_result = None

        global plot_n
        plot_n = 0

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

        LogWriter.log(f"        ordering tables...")

        # sorts the dataframe by subject to make sure it has the same subjects
        df1.sort_index(inplace=True)
        df2.sort_index(inplace=True)

        return df1, df2

    def bland_altmann(self, data=("aseg", "aparcL", "aparcR"), c_to_keep=None, n_subplots=4, n_rows=2,
                      c_to_exclude=("ID")):

        if not self.subjects_list:
            LogWriter.log("bland altmannn: datasets do not have elements in common")
            return

        for d in data:
            img_name = f"{self.data_path}images\\img_{d}_ba_{self.name}"
            self.iterate(self.__bland_altman_plot, d, c_to_keep, n_subplots, n_rows, c_to_exclude, img_name)

    def violin(self, data=("aseg", "aparcL", "aparcR"), c_to_keep=None, n_subplots=10, n_rows=2, c_to_exclude=("ID")):

        for d in data:
            img_name = f"{self.data_path}images\\img_{d}_violin_{self.name}"
            self.iterate(self.__violin_plot, d, c_to_keep, n_subplots, n_rows, c_to_exclude, img_name)

    def iterate(self, function, data, c_to_keep, n_subplots, n_rows, c_to_exclude, img_name):
        plots_n = 0
        fig, axs = None, None

        df1, df2 = self.get_table(data)

        columns_list = set(df1.columns.tolist()).intersection(
            set(df2.columns.tolist()))

        if c_to_keep is not None:
            columns = [x for x in columns_list if x in c_to_keep]
        else:
            columns = columns_list

        if function.__name__ == "__bland_altman_plot":
            df1, df2 = self.__match_dataframes(df1, df2)

        not_done = []
        for i, column_to_compare in enumerate(columns):
            if column_to_compare not in c_to_exclude:
                a = pd.to_numeric(df1.loc[:, column_to_compare], errors='coerce')
                b = pd.to_numeric(df2.loc[:, column_to_compare], errors='coerce')

                if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                    if not plots_n % n_subplots:
                        # plots when
                        if plots_n > 1:
                            if fig is not None:
                                fig.savefig(f"{img_name}"
                                            f"_{str(plots_n - n_subplots)}-{str(plots_n)}.png")  # save the figure to file

                        fig, axs = self.create_plot(n_subplots, n_rows)

                    if function is not None:
                        function(axs[plots_n % n_subplots], a, b, title=a.name + "\n" + self.name)
                    plots_n += 1

                else:
                    not_done.append(a.name)
                    # LogWriter.log(f"        excluded {column_to_compare}")

                if plots_n >= self.max_plot:  # to avoid plotting too much
                    break

        if plots_n % n_subplots != 0:
            if fig is not None:
                fig.savefig(f"{img_name}"
                            f"_{str(plots_n - (plots_n % n_subplots))}-{str(plots_n)}.png")  # save the figure to file
                del axs, fig

        LogWriter.log(f"    {self.name} - plotted for {plots_n} variables out of {i + 1}")
        not_done_str = ' | '.join(not_done)
        LogWriter.log(f"    skipped: {not_done_str}")

    def get_table(self, data):
        # if data == "aseg":
        #     _df1 = self.stat_df_1.df_stats_aseg[self.stat_df_1.df_stats_aseg["ID"].isin(self.subjects_list)]
        #     _df2 = self.stat_df_2.df_stats_aseg[self.stat_df_2.df_stats_aseg["ID"].isin(self.subjects_list)]
        # elif data == "aparcR":
        #     _df1 = self.stat_df_1.df_stats_aparcL[self.stat_df_1.df_stats_aparcL["ID"].isin(self.subjects_list)]
        #     _df2 = self.stat_df_2.df_stats_aparcL[self.stat_df_2.df_stats_aparcL["ID"].isin(self.subjects_list)]
        # elif data == "aparcL":
        #     _df1 = self.stat_df_1.df_stats_aparcR[self.stat_df_1.df_stats_aparcR["ID"].isin(self.subjects_list)]
        #     _df2 = self.stat_df_2.df_stats_aparcR[self.stat_df_2.df_stats_aparcR["ID"].isin(self.subjects_list)]
        # else:
        #     raise "wrong selection parameter"
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
            raise "wrong selection parameter"
        return _df1, _df2

    @staticmethod
    def create_plot(n_subplots, n_rows):

        fig, axs = plt.subplots(n_rows, int(n_subplots / n_rows), figsize=(40, 20))
        axs = axs.ravel()
        plt.subplots_adjust(hspace=0.5)
        plt.subplots_adjust(wspace=0.2)

        return fig, axs

    def __violin_plot(self, _ax, _a, _b, title):
        # Create a DataFrame with the two Series
        # df = pd.DataFrame({'Freesurfer': _a, 'Fastsurfer': _b})

        df = pd.DataFrame({'Data': pd.concat([_a, _b]),
                           'Group': [self.categories[0]] * len(_a) + [self.categories[1]] * len(_b),
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
        # mean_list = []
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

    def __correction_param(self):
        return self.alpha / len(self.stat_df_result)

    def stat_test(self, c_to_exclude=None, data=("aseg", "aparcL", "aparcR")):
        """
        :param c_to_exclude:
        :param columns: list of str - list of column names to print (default None: prints all)
        :param data: str - type of input (aseg, aparcL or aparcR)
        :return: void
        """
        if c_to_exclude is None:
            c_to_exclude = set()

        r_all = []
        for d in data:
            _df1, _df2 = self.get_table(d)

            _df1, _df2 = self.__match_dataframes(_df1, _df2)

            LogWriter.log(f"t_test and mann whitney on {d} in {self.name}...")

            # se non viene dato un input fa il test per tutte le colonne
            if not c_to_exclude:
                columns = set(_df1.columns.tolist()).intersection(set(_df2.columns.tolist()))
            else:
                columns = c_to_exclude

            not_done = []
            for i, column_to_compare in enumerate(columns):
                if column_to_compare not in c_to_exclude:
                    a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                    b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')

                    if len(a) != len(b):
                        LogWriter.log(f"        len a: {len(a)} len b: {len(b)}")
                        not_done.append(column_to_compare)
                        continue

                    if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):

                        r1, p1, o1 = self.__wilcoxon(a, b)
                        r2, p2, o2 = self.__t_test(a, b)
                        cd, rd = self.__cohens_d(a, b)
                        # ICC

                        if isinstance(column_to_compare, int):
                            column_to_compare_name = _df1.columns[column_to_compare]

                            r_all.append({"name": f"{self.name}_{d}_{column_to_compare_name}",
                                          "wilcoxon": {"result": r1,
                                                       "p_value": p1,
                                                       "outcome": o1},
                                          "t_test": {"result": r2,
                                                     "p_value": p2,
                                                     "outcome": o2},
                                          "d": {"result": rd,
                                                "d_value": cd}})

                        if isinstance(column_to_compare, str):
                            r_all.append({"name": f"{self.name}_{d}_{column_to_compare}",
                                          "wilcoxon": {"result": r1,
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

            LogWriter.log(f"    failed {len(not_done)} variables out of {len(columns)}")
            not_done_str = ' | '.join(not_done)
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
            if type(row["wilcoxon p_value"]) is not str and type(row["wilcoxon p_value"]) is not str and type(
                    self.updated_alpha) is not str:
                if row["wilcoxon p_value"] < self.updated_alpha:
                    row[
                        "wilcoxon message"] = f"p-value: {row['wilcoxon p_value']} - null hypothesis " \
                                              f"rejected, means are not statistically equal "
                    row["wilcoxon outcome"] = 1
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
                [self.stat_df_result, pd.DataFrame({"wilcoxon p_value": item["wilcoxon"]["p_value"],
                                                    "wilcoxon outcome": item["wilcoxon"]["outcome"],
                                                    "wilcoxon message": item["wilcoxon"]["result"],
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
    def __wilcoxon(_a, _b):
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


class Recap:

    def __init__(self):
        self.df = pd.DataFrame()

    def add_line(self, list):
        row = pd.series(list)

        self.df.appen(row)

    def save(self, filename="dataframe.csv"):
        self.df.to_csv(filename)
