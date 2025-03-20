import os
from FastsurferTesting_pc import Table, Stats, LogWriter
import pandas as pd
import matplotlib.pyplot as plt









class Comparison2:
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

        global n_plot
        n_plot = 0

    def iterate(self, data, columns, n_subplots, n_rows, c_to_exclude):
        for d in data:
            df1, df2 = self.get_table(d)

            not_done = []
            for column_to_compare in self.columns_list:
                if column_to_compare not in c_to_exclude:
                    a = pd.to_numeric(_df1.loc[:, column_to_compare], errors='coerce')
                    b = pd.to_numeric(_df2.loc[:, column_to_compare], errors='coerce')

                    if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                        pass

    def violin(self, data="aseg", columns=None, n_subplots=10, n_rows=2, c_to_exclude=[]):

        """
        :param data: str - table to select (aseg, aparcL, aparcR)
        :param columns: list  of str- list of column names to print (default None: prints all)
        :param n_subplots: int - n of subplots in image (default 4)
        :param n_rows: int - n of rows in plot (default 2)
        :return: void
        """
        plots = 0

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
            raise "violin: wrong selection parameter"

        LogWriter.log(f"Violin plot: {self.name}")
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

    def bland_altmann(self, data="aseg", columns=None, n_subplots=4, n_rows=2, c_to_exclude=[]):

    def get_table(self, data):
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
            raise "violin: wrong selection parameter"

        return _df1, _df2