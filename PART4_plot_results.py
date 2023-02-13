import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

ROWS_TO_PLOT = range(91,100)  # from the statistical test csv file
N_SUBPLOTS = 4
N_PLOT_ROWS = 2


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def plot_from_csv(base_path, csv):
    plots = 0
    # plt.ion()
    df = pd.read_csv(base_path + csv)

    for index, row in df.iterrows():
        if not ROWS_TO_PLOT:
            if row[3]:
                if not plots % N_SUBPLOTS:
                    fig, axs = plt.subplots(N_PLOT_ROWS, int(N_SUBPLOTS / N_PLOT_ROWS), figsize=(40, 20))
                    axs = axs.ravel()
                    # mng = plt.get_current_fig_manager()
                    # mng.full_screen_toggle()

                # print(plots % N_SUBPLOTS)
                plot(axs[plots % N_SUBPLOTS], row, base_path)
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
                plot(axs[plots % N_SUBPLOTS], row, base_path)
                plots += 1

            if plots >= 29:  # to avoid plotting too much
                break

    plt.show()


def plot(axes, row, base_path):
    info = row[0].split(" ")
    filename = info[0]
    column_to_compare = info[1]

    filename1 = "Stats_Freesurfer/" + filename
    filename2 = "Stats_FastSurfer/" + filename

    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)

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
    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
    csv = "test_results.csv"

    plot_from_csv(base_path, csv)
