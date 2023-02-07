import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

SIGNIFICANCE_THRESHOLD = 0.05


def plot_measures(series1, series2, title, ticklabels):
    x = np.linspace(1, 20, num=20)

    plt.plot(x, series1, 'ro', x, series2, 'bo')
    plt.vlines(x, ymin=0, ymax=4000, linestyles='dotted')
    plt.xticks(range(1, 21), labels=ticklabels, rotation=70, ha="center")
    plt.title(title)
    plt.legend(['Freesurfer', 'Fastsurfer'])
    plt.show()


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def t_test(base_path, filename1, filename2, column_to_compare):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)
    # print(base_path + filename1 + filename2)

    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]

    a, b = get_column(column_to_compare, df1, df2)

    # a = df1.loc[:, column_to_compare]
    # b = df2.loc[:, column_to_compare]
    # # print(a)
    # # print(b)

    if "NaN" in a or "NaN" in b:
        return "result could not be computed", "NaN", "NaN"

    t_stat, p_value = stats.ttest_ind(a, b)

    # p value is the likelihood that these are the same
    # print("t test")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
        outcome = 0
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"
        outcome = 1
        # plot_measures(a, b, column_to_compare, df1.loc[:, "subjects"].tolist())

    # print(result)
    return result, p_value, outcome


def mann_whitney(base_path, filename1, filename2, column_to_compare):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)
    # print(base_path + filename1 + filename2)

    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]
    # p rint(df1.head())
    # print(df2.head())

    a, b = get_column(column_to_compare, df1, df2)

    if "NaN" in a or "NaN" in b:
        return "result could not be computed", "NaN", "NaN"

    # if isinstance(column_to_compare, int):
    #     a = df1.iloc[:, column_to_compare]
    #     b = df2.iloc[:, column_to_compare]
    #
    # if isinstance(column_to_compare, str):
    #     a = df1.loc[:, column_to_compare]
    #     b = df2.loc[:, column_to_compare]

    df1.to_csv("dataset_uniti_test.csv", index=False)
    # print(a)
    # print(b)

    t_stat, p_value = stats.mannwhitneyu(a, b)

    # p value is the likelihood that these are the same
    # print("Mann Whitney")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
        outcome = 0
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"
        outcome = 1
        # plot_measures(a, b, column_to_compare, df1.loc[:, "subjects"].tolist())
    # print(result)
    return result, p_value, outcome


def save(list_line):
    file = []
    for item in list_line:
        file.append(item["name"])
        file.append("\t" + item["mann_whitney"])
        file.append("\t" + item["t_test"])
        file.append("\n")
    dm.write_txt(file, "test_results.txt")


def save_csv(list_line):
    df = pd.DataFrame()

    for item in list_line:
        df = pd.concat([df, pd.DataFrame({"mann_whitney p_value": item["mann_whitney"]["p_value"],
                                          "mann_whitney outcome": item["mann_whitney"]["outcome"],
                                          "mann_whitney message": item["mann_whitney"]["result"],
                                          "t_test p_value": item["t_test"]["p_value"],
                                          "t_test outcome": item["t_test"]["outcome"],
                                          "t_test message": item["t_test"]["result"],
                                          "significance_threshold_used": SIGNIFICANCE_THRESHOLD
                                          }, index=[item["name"]])])

    df.to_csv("test_results.csv")  # , index=False


def stat_test(base_path, filename1, filename2, column_to_compare, r_all):
    r1, p1, o1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2, p2, o2 = t_test(base_path, filename1, filename2, column_to_compare)

    if isinstance(column_to_compare, int):
        df_example = pd.read_csv(base_path + filename2)
        column_to_compare_name = df_example.columns[column_to_compare]

        r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare_name}",
                      "mann_whitney": {"result": r1,
                                       "p_value": p1,
                                       "outcome": o1},
                      "t_test": {"result": r2,
                                 "p_value": p2,
                                 "outcome": o2}})
        del df_example

    if isinstance(column_to_compare, str):
        r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                      "mann_whitney": {"result": r1,
                                       "p_value": p1,
                                       "outcome": o1},
                      "t_test": {"result": r2,
                                 "p_value": p2,
                                 "outcome": o2}})


def main():
    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"

    r_all = []

    filename1 = "Stats_Freesurfer/aseg_AD.csv"
    filename2 = "Stats_FastSurfer/aseg_AD.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    filename1 = "Stats_Freesurfer/aseg_healthy.csv"
    filename2 = "Stats_FastSurfer/aseg_healthy.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"

    max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
    for column_to_compare in range(2, max_len):
        stat_test(base_path, filename1, filename2, column_to_compare, r_all)

    save_csv(r_all)


def main_old():
    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
    """
    test order
    aseg 
        AD left hippocampus volume
        AD right hippocampus volume
        healthy left hippocampus volume
        healthy right hippocampus volume
        
    aparc 
        AD left parahippocampal thickness
        AD right parahippocampal thickness
        healthy left parahippocampal thickness
        healthy right parahippocampal thickness
    
    """
    r_all = []

    filename1 = "Stats_Freesurfer/aseg_AD.csv"
    filename2 = "Stats_FastSurfer/aseg_AD.csv"

    column_to_compare = "Left-Hippocampus volume_mm3"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    column_to_compare = "Left-Hippocampus volume_mm3"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})
    column_to_compare = "Right-Hippocampus volume_mm3"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aseg_healthy.csv"
    filename2 = "Stats_FastSurfer/aseg_healthy.csv"

    column_to_compare = "Left-Hippocampus volume_mm3"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    column_to_compare = "Right-Hippocampus volume_mm3"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
    column_to_compare = "parahippocampal_mean_thickness_mm"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
    column_to_compare = "parahippocampal_mean_thickness_mm"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
    column_to_compare = "parahippocampal_mean_thickness_mm"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
    column_to_compare = "parahippocampal_mean_thickness_mm"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
    column_to_compare = "parahippocampal_mean_area_mm2"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
    column_to_compare = "parahippocampal_mean_area_mm2"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
    column_to_compare = "parahippocampal_mean_area_mm2"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
    column_to_compare = "parahippocampal_mean_area_mm2"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    # save(r_all)


if __name__ == "__main__":
    main()
