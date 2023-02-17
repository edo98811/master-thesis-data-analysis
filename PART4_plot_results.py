import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

ROWS_TO_PLOT = range(91, 100)  # from the statistical test csv file
N_SUBPLOTS = 4
N_PLOT_ROWS = 2
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
SUBJ_TABLE = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/text_and_csv_files/OASIS_table.csv"
COLUMNS_TO_PLOT = 0


def main():
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


"""
DESCRIPTION
    
    plot from csv
    
    plot subplot 
    
    plot violinplot 
    
    get column 
    
    this script i used to make a plot of the data computed from the previous scripts
    it can do
    a violin plot 
    
    a plot for single subects

"""


def violin_plot(ax, _a, _b):
    # Create a DataFrame with the two Series
    df = pd.DataFrame({'Freesurfer': _a, 'Fastsurfer': d_b})

    # Create a split violin plot
    # sns.violinplot(data=df, split=True)
    sns.violinplot(ax=ax, data=df,
                   split=True)


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

        for a_column, b_column in zip(_df1_filtered.iloc[:, 2:], _df2_filtered.iloc[:, 2:]):

            a = _df1_filtered.loc[:,a_column]
            b = _df2_filtered.loc[:,b_column]

            if a.any() and b.any():
                if not plots % N_SUBPLOTS:
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                if axs:
                    violin_plot(axs[plots % N_SUBPLOTS], a, b)
                plots += 1

            if plots >= 29:  # to avoid plotting too much
                break

    plt.show()


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

    plt.show()


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def plot(axes, row):
    info = row[0].split(" ")\
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


if __name__ == "__main__":
    main()
