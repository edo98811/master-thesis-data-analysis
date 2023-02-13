import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"


def main():
    r_all = []

    df1 = pd.read_csv("Stats_Freesurfer/aseg.csv")
    df2 = pd.read_csv("Stats_FastSurfer/aseg.csv")

    max_len = min(len(df1.axes[1]), len(df2.axes[1]))

    subjects_list = df2.query("dx1=='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)

    subjects_list = df2.query("dx1!='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)

    df1 = pd.read_csv("Stats_Freesurfer/aparcDKT_right.csv")
    df2 = pd.read_csv("Stats_FastSurfer/aparcDKT_right.csv")

    max_len = min(len(df1.axes[1]), len(df2.axes[1]))

    subjects_list = df2.query("dx1=='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)

    subjects_list = df2.query("dx1!='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)

    df1 = pd.read_csv("Stats_Freesurfer/aparcDKT_left.csv")
    df2 = pd.read_csv("Stats_FastSurfer/aparcDKT_left.csv")

    max_len = min(len(df1.axes[1]), len(df2.axes[1]))

    subjects_list = df2.query("dx1=='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)

    subjects_list = df2.query("dx1!='Cognitively Normal'")["ID"].tolist()
    for column_to_compare in range(2, max_len):
        stat_test(BASE_PATH, df1, df2, column_to_compare, r_all, subjects_list)
"""
description 

    PART 3: do a statistical test on the results obtained from the fastsufer and freesurfer processing

        
    stat test: runs the statistical tests and saves the output in a dictionary, the name of the statistic compard is saved even if nmumbers are used  as indexes
        - input 
            basepath 
            filename 1
            filename 2
            column to compare
            
        - output 
            stat test data structure 
        

        
    save to csv 
        
    before running
        have the tables created using the fastsrfer and freesurfer stat script, they dont need to be the same subjects because 
        here only subjects that exist in both tables are used 
        for each comparison that you want to run the file must be selected and also the columns that have the stats you want to comppare
        the columns can be chosen both by number or by name 
        
    main
        the only need here is to call the stat test function providing all the necessary parameters
        the output of the function must be saved in a list or a single value (it is a dictionary and can be saved using the 
        save_csv function)
        
    save to csv 
    
    
"""
SIGNIFICANCE_THRESHOLD = 0.05


def stat_test(base_path, filename1, filename2, column_to_compare, subjs_list, r_all):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)

    r1, p1, o1 = mann_whitney(df1, df2, column_to_compare)
    r2, p2, o2 = t_test(df1, df2, column_to_compare)

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


def save_csv(base_path, list_line):
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

    df.to_csv(base_path + "test_results.csv")  # , index=False


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def t_test(df1, df2, column_to_compare):
    a, b = get_column(column_to_compare, df1, df2)

    if "NaN" in a or "NaN" in b:
        print("could not compute")
        return "result could not be computed", "NaN", "NaN"

    t_stat, p_value = stats.ttest_ind(a, b)

    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
        outcome = 0
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"
        outcome = 1

    return result, p_value, outcome


def mann_whitney(df1, df2, column_to_compare):
    a, b = get_column(column_to_compare, df1, df2)

    if "NaN" in a or "NaN" in b:
        return "result could not be computed", "NaN", "NaN"

    df1.to_csv("dataset_uniti_test.csv", index=False)

    t_stat, p_value = stats.mannwhitneyu(a, b)

    # p value is the likelihood that these are the same
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
        outcome = 0
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"
        outcome = 1

    return result, p_value, outcome

## OLD FILES
def save_txt(list_line):
    file = []
    for item in list_line:
        file.append(item["name"])
        file.append("\t" + item["mann_whitney"])
        file.append("\t" + item["t_test"])
        file.append("\n")
    dm.write_txt(file, "old scripts/test_results.txt")


def main_old_2():
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

    save_csv(base_path,
             r_all)


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
