import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

results = []


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
    print(base_path + filename1 + filename2)

    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]

    a, b = get_column(column_to_compare, df1, df2)

    # a = df1.loc[:, column_to_compare]
    # b = df2.loc[:, column_to_compare]
    # # print(a)
    # # print(b)

    t_stat, p_value = stats.ttest_ind(a, b)

    # p value is the likelihood that these are the same
    print("t test")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"
        plot_measures(a, b, column_to_compare, df1.loc[:, "subjects"].tolist())

    print(result)
    return result

def mann_whitney(base_path, filename1, filename2, column_to_compare):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)
    print(base_path + filename1 + filename2)

    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]
    print(df1.head())
    print(df2.head())

    a, b = get_column(column_to_compare, df1, df2)

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
    print("Mann Whitney")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"
        plot_measures(a, b, column_to_compare, df1.loc[:, "subjects"].tolist())
    print(result)
    return result


def save(list_line):
    file = []
    for item in list_line:
        file.append(item["name"])
        file.append("\t" + item["mann_whitney"])
        file.append("\t" + item["t_test"])
        file.append("\n")
    dm.write_txt(file, "test_results.txt")

def stat_test(base_path, filename1, filename2, column_to_compare, r_all):
    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})


if __name__ == "__main__":
    main()

def main():
    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
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

    save(r_all)
