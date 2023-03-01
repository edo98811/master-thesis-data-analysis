import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ROWS_TO_PLOT = range(91, 100)  # from the statistical test csv file
N_SUBPLOTS_V = 10
N_SUBPLOTS_BA = 4
N_PLOT_ROWS = 2
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
SUBJ_TABLE = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/text_and_csv_files/OASIS_table.csv"
COLUMNS_TO_PLOT = 0


def omain():
    # csv = "test_results.csv"
    #
    # plot_from_csv(csv)

    global subj_table
    subj_table = pd.read_csv(SUBJ_TABLE)

    print(subj_table.head())

    global queries
    queries = ["main_condition=='Cognitively normal'", "main_condition!='Cognitively normal'"]

    global df1_path
    df1_path = "Stats_FreeSurfer/aseg.csv"
    global df2_path
    df2_path = "Stats_FastSurfer/aseg.csv"

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)
    violin_preprocsessing()
    bland_altmann_preprocessing()


def otherMain():
    df1_path = "Stats_FreeSurfer/aparcDKT_right.csv"

    df2_path = "Stats_FastSurfer/aparcDKT_right.csv"

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)
    violin_preprocsessing()
    bland_altmann_preprocessing()
    df1_path = "Stats_FreeSurfer/aparcDKT_left.csv"

    df2_path = "Stats_FastSurfer/aparcDKT_left.csv"

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)
    violin_preprocsessing()
    bland_altmann_preprocessing()


def main():
    global subj_table
    subj_table = pd.read_csv(SUBJ_TABLE)

    print(subj_table.head())

    global queries
    queries = ["main_condition=='Cognitively normal'", "main_condition!='Cognitively normal'"]

    global df1_path

    global df2_path

    df1_path = "Stats_FreeSurfer/aparcDKT_right.csv"

    df2_path = "Stats_FastSurfer/aparcDKT_right.csv"

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)
    violin_preprocsessing()
    bland_altmann_preprocessing()

    df1_path = "Stats_FreeSurfer/aparcDKT_left.csv"

    df2_path = "Stats_FastSurfer/aparcDKT_left.csv"

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)
    violin_preprocsessing()
    bland_altmann_preprocessing()



#  plt.show()
"""
DESCRIPTION
    violin plot 
    
    violin preprocessing 
    
    bland altmann plot 
    
    bland altmann preprocessing
    
    plot from csv
    
    plot subplot 
    
    plot violinplot 
    
    get column 
    
    this script i used to make a plot of the data computed from the previous scripts
    it can do
    a violin plot 
    
    a plot for single subects

"""


def violin_preprocsessing():
    plots = 0
    # plt.ion()
    _df1 = pd.read_csv(BASE_PATH + df1_path)
    _df2 = pd.read_csv(BASE_PATH + df2_path)

    for query in queries:

        # filter according to the query the subjects in the table with the list of all subjects
        subjects_list = subj_table.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s

        _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]  # healthy or not healthy free
        _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]  # healthy or not healthy fast

        c_names_list = _df1_filtered.columns
        c_names_list = c_names_list.intersection(_df2_filtered.columns).tolist()

        c_names = set(c_names_list)
        for c in c_names:
            # a_column, b_column in zip(_df1_filtered.iloc[:, 2:], _df2_filtered.iloc[:, 2:]):

            a = pd.to_numeric(_df1_filtered.loc[:, c], errors='coerce')
            b = pd.to_numeric(_df2_filtered.loc[:, c], errors='coerce')
            # print(a)
            # print(b)
            # print(f"{a_column} {b_column}")
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                if not plots % N_SUBPLOTS_V:
                    if plots > 1:
                        fig.savefig(BASE_PATH + "/images_2/img_violin_" + df2_path.split("/")[-1][:-4] + "_" + str(
                            plots) + ".png")  # save the figure to file
                        # plt.close(fig)  # close the figure window
                        # handles, labels = axs[1].get_legend_handles_labels()
                        # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
                        plt.close()
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS_V / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()
                    plt.subplots_adjust(hspace=0.5)
                    plt.subplots_adjust(wspace=0.2)
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)

                violin_plot(axs[plots % N_SUBPLOTS_V], a, b)
                plots += 1

            if plots >= 100:  # to avoid plotting too much
                break


def violin_plot(ax, _a, _b):
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


def bland_altmann_preprocessing():
    plots = 0
    # plt.ion()
    _df1 = pd.read_csv(BASE_PATH + df1_path)
    _df2 = pd.read_csv(BASE_PATH + df2_path)

    for query in queries:

        # filter according to the query the subjects in the table with the list of all subjects
        subjects_list = subj_table.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s

        _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]  # healthy or not healthy free
        _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]  # healthy or not healthy fast

        c_names_list = _df1_filtered.columns
        c_names_list = c_names_list.intersection(_df2_filtered.columns).tolist()

        c_names = set(c_names_list)
        for c in c_names:
            # a_column, b_column in zip(_df1_filtered.iloc[:, 2:], _df2_filtered.iloc[:, 2:]):

            a = pd.to_numeric(_df1_filtered.loc[:, c], errors='coerce')
            b = pd.to_numeric(_df2_filtered.loc[:, c], errors='coerce')
            # print(a)
            # print(b)
            # print(f"{a_column} {b_column}")
            if a.any() and b.any() and (a.notnull().all() and b.notnull().all()):
                if not plots % N_SUBPLOTS_BA:
                    if plots > 1:
                        fig.savefig(BASE_PATH + "/images_2/img_ba_" + df2_path.split("/")[-1][:-4] + "_" + str(
                            plots) + ".png")  # save the figure to file
                        # handles, labels = ax.get_legend_handles_labels()
                        # fig.legend(handles, labels, loc=(0.95, 0.1), prop={'size': 30})
                        plt.close()
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS_BA / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()
                    plt.subplots_adjust(hspace=0.5)
                    plt.subplots_adjust(wspace=0.2)
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                bland_altman_plot(axs[plots % N_SUBPLOTS_BA], a, b)
                plots += 1

            if plots >= 400:  # to avoid plotting too much
                break


def bland_altman_plot(ax, _a, _b):
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


def plot_from_csv(csv):
    plots = 0
    # plt.ion()
    df = pd.read_csv(BASE_PATH + csv)

    for index, row in df.iterrows():
        if not ROWS_TO_PLOT:
            if row[3]:
                if not plots % N_SUBPLOTS:
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                plot(axs[plots % N_SUBPLOTS], row)
                plots += 1
        else:
            if index in ROWS_TO_PLOT:
                if not plots % N_SUBPLOTS:
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()

                    plt.subplots_adjust(hspace=0.6)
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                plot(axs[plots % N_SUBPLOTS], row)
                plots += 1

            if plots >= 29:  # to avoid plotting too much
                break


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def plot(axes, row):
    info = row[0].split(" ")
    filename = info[0]
    column_to_compare = info[1]

    filename1 = "Stats_Freesurfer/" + filename
    filename2 = "Stats_FastSurfer/" + filename

    df1 = pd.read_csv(BASE_PATH + filename1)
    df2 = pd.read_csv(BASE_PATH + filename2)

    # se includo ADNI devo aggiungere roba
    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]

    a, b = get_column(column_to_compare, df1, df2)
    if len(a) == len(b) and len(a) == len(df1.loc[:, "subjects"].tolist()):
        plot_measures(a, b, row[0].replace(" ", "\n"), df1.loc[:, "subjects"].tolist(), axes)


def plot_measures(series1, series2, title, ticklabels, ax=None):
    x = np.linspace(1, len(ticklabels), num=len(ticklabels))
    if not ax:
        ax = plt.figure

    ax.plot(x, series1, 'ro', x, series2, 'bo')
    y_min = min(pd.concat([series1, series2]))
    y_max = max(pd.concat([series1, series2]))
    diff = y_max - y_min
    ax.vlines(x, ymin=y_min - diff, ymax=y_max + diff, linestyles='dotted')
    ax.vlines(x, ymin=series1, ymax=series2)
    ax.set_xticks(range(1, len(ticklabels) + 1), labels=ticklabels, rotation=45, ha="right")
    # ax.xticks(range(1, 21), labels=ticklabels, rotation=70, ha="center")
    ax.title.set_text(title)
    # ax.title(title)
    ax.legend(['Freesurfer', 'Fastsurfer'])

    plt.draw()


def violin_plots(ax, _queries, _df1_path, _df2_path, _subj_table):
    _df1 = pd.read_csv(BASE_PATH + _df1_path)
    _df2 = pd.read_csv(BASE_PATH + _df2_path)
    for query in _queries:

        subjects_list = _subj_table.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s

        _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]
        _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]

        # Split violin plot
        sns.violinplot(ax=ax, data=pd.concat([_df2_filtered, _df1_filtered], ignore_index=True).iloc[:, 1:6],
                       split=True)


if __name__ == "__main__":
    main()
