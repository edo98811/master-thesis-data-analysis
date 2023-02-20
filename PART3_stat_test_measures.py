import data_manipulation as dm
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
SUBJ_TABLE = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/text_and_csv_files/OASIS_table.csv"


def main():
    r_all = []
    subj_table = pd.read_csv(SUBJ_TABLE)

    print(subj_table.head())
    queries = ["main_condition=='Cognitively normal'", "main_condition!='Cognitively normal'"]

    stat_test(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table, r_all)
    stat_test(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table, r_all)
    stat_test(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table, r_all)

    # violin_plots(queries, "Stats_FreeSurfer/aseg.csv", "Stats_FastSurfer/aseg.csv", subj_table)


def violin_plots(_queries, _df1_path, _df2_path, _subj_table):
    _df1 = pd.read_csv(BASE_PATH + _df1_path)
    _df2 = pd.read_csv(BASE_PATH + _df2_path)
    for query in _queries:

        subjects_list = _subj_table.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s

        _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]
        _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]

        # Split violin plot
        sns.violinplot(data=pd.concat([_df2_filtered, _df1_filtered], ignore_index=True).iloc[:, 1:6], split=True)

    # table_tested_name = _df1_path.split(".")[-2]
    # normal = df.loc[df['main_condition'] == 'Cognitively normal']
    # not_normal = df.loc[df['main_condition'] != 'Cognitively normal']

    """
    dataset che mi serve
    y: età
    x: area 

    split: condition 

    """
    plt.show()

"""
description 

    PART 3: do a statistical test on the results obtained from the fastsufer and freesurfer processing

        
    stat test: runs the statistical tests and saves the output in a dictionary, the name of the statistic compard is saved even if nmumbers are used  as indexes
        - input 
            queries list 
            filename 1
            filename 2
            subjects table
            column to compare
            
        - output 
            saves the table wiht the query passed with te query name 
        
    description 
        loads the datasets
        then iterates through all the queries 
        filter the datasets according to the subjects that are in both taht respect the query
        for each column performs the test
        saves the result in a dictionary 
        converts the dictionary in dataframe and then csv

        
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
    
    update 20/02 added bonferroni correction 
"""
SIGNIFICANCE_THRESHOLD = 0.05
def bonferroni_correction_param(queries):
    tot = 0
    for query in queries:
        with open(BASE_PATH + query + ".csv") as fp:
            for (count, _) in enumerate(fp, 1):
                pass
            print("count")
            tot += count

     return SIGNIFICANCE_THRESHOLD / tot

def bonferroni_correction(queries):
    updated_ST = bonferroni_correction_param(queries)
    for query in queries:
        df = pd.read_csv(BASE_PATH + query + ".csv")
        for i, row in enumerate(df.rows):
            if row[0] < updated_ST:
                row[1] = f"p-value: {row[0]} - null hypothesis rejected, means are not statistically equal"
                row[2] = 1
            if row[3] < updated_ST:
                row[4] = f"p-value: {row[3]} - null hypothesis rejected, the datasets have a different distribution"
                row[5] = 1
            df.iloc[i,:] = row
        df.to_csv(BASE_PATH + f"{query}_bonferroni_corrected.csv")

def stat_test(_queries, _df1_path, _df2_path, _subj_table, r_all):
    # input: query, df1 name, df2 name, subj_table, list of all test results
    _df1 = pd.read_csv(BASE_PATH + _df1_path)
    _df2 = pd.read_csv(BASE_PATH + _df2_path)

    table_tested_name = _df1_path.split(".")[-2]

    max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
    for query in _queries:

        subjects_list = _subj_table.query(query)["ID"].tolist()
        for i, s in enumerate(subjects_list):
            subjects_list[i] = "sub-" + s
        print(f"query -> {query} on table returned these values:")
        print(subjects_list)
        print("dataset 1 not filtered")
        print(_df1.head())

        _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]
        _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]

        print("filtered dataset 1 according to subjects returned in queries")
        print(_df2_filtered.head())
        print("filtered dataset 2")
        print(_df2_filtered.head())
        print("COMPUTING STATS FOR FIRST QUERY...")

        for column_to_compare in range(2, max_len):
            a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
            if a.any() and b.any():
                r1, p1, o1 = mann_whitney(a, b)
                r2, p2, o2 = t_test(a, b)

                if isinstance(column_to_compare, int):
                    column_to_compare_name = _df1_filtered.columns[column_to_compare]

                    r_all.append({"name": f"{table_tested_name} {column_to_compare_name}",
                                  "mann_whitney": {"result": r1,
                                                   "p_value": p1,
                                                   "outcome": o1},
                                  "t_test": {"result": r2,
                                             "p_value": p2,
                                             "outcome": o2}})

                if isinstance(column_to_compare, str):
                    r_all.append({"name": f"{table_tested_name} {column_to_compare}",
                                  "mann_whitney": {"result": r1,
                                                   "p_value": p1,
                                                   "outcome": o1},
                                  "t_test": {"result": r2,
                                             "p_value": p2,
                                             "outcome": o2}})
            else:
                print(f"no data in category {column_to_compare}")
        save_csv(r_all, f"{query}.csv")


def save_csv(list_to_save, _name):
    df = pd.DataFrame()

    for item in list_to_save:
        df = pd.concat([df, pd.DataFrame({"mann_whitney p_value": item["mann_whitney"]["p_value"],
                                          "mann_whitney outcome": item["mann_whitney"]["outcome"],
                                          "mann_whitney message": item["mann_whitney"]["result"],
                                          "t_test p_value": item["t_test"]["p_value"],
                                          "t_test outcome": item["t_test"]["outcome"],
                                          "t_test message": item["t_test"]["result"],
                                          "significance_threshold_used": SIGNIFICANCE_THRESHOLD
                                          }, index=[item["name"]])])

    df.to_csv(BASE_PATH + _name)  # , index=False


def get_column(column_to_compare, df1, df2):
    if isinstance(column_to_compare, int):
        a = df1.iloc[:, column_to_compare]
        b = df2.iloc[:, column_to_compare]

    if isinstance(column_to_compare, str):
        a = df1.loc[:, column_to_compare]
        b = df2.loc[:, column_to_compare]

    return a, b


def t_test(a, b):
    # a, b = get_column(column_to_compare, df1, df2)

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


def mann_whitney(a, b):
    # a, b = get_column(column_to_compare, df1, df2)

    if "NaN" in a or "NaN" in b:
        return "result could not be computed", "NaN", "NaN"

    # df1.to_csv("dataset_uniti_test.csv", index=False)

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
# def stat_test_old(_df1, _df2, column_to_compare, file_tested_name, r_all):
#     a, b = get_column(column_to_compare, _df1, _df2)
#
#     r1, p1, o1 = mann_whitney(a, b)
#     r2, p2, o2 = t_test(a, b)
#
#     if isinstance(column_to_compare, int):
#         column_to_compare_name = _df1.columns[column_to_compare]
#
#         r_all.append({"name": f"{file_tested_name} {column_to_compare_name}",
#                       "mann_whitney": {"result": r1,
#                                        "p_value": p1,
#                                        "outcome": o1},
#                       "t_test": {"result": r2,
#                                  "p_value": p2,
#                                  "outcome": o2}})
#
#     if isinstance(column_to_compare, str):
#         r_all.append({"name": f"{file_tested_name} {column_to_compare}",
#                       "mann_whitney": {"result": r1,
#                                        "p_value": p1,
#                                        "outcome": o1},
#                       "t_test": {"result": r2,
#                                  "p_value": p2,
#                                  "outcome": o2}})

# def main_old():
#     r_all = []
#
#     # load subjects info table and select processed subjects
#     subj_table = pd.read_csv(SUBJ_TABLE)
#
#     # filter results
#     df1 = pd.read_csv(BASE_PATH + "Stats_Freesurfer/aseg.csv")
#     df2 = pd.read_csv(BASE_PATH + "Stats_FastSurfer/aseg.csv")
#
#     table_name = df1.split(".")[-2]
#
#     max_len = min(len(df1.axes[1]), len(df2.axes[1]))
#     subjects_list = subj_table.query("'main_condition'=='Cognitively Normal'")["ID"].tolist()
#     df1 = df1.loc[df1['ID'].isin([subjects_list])]
#     df2 = df2.loc[df2['ID'].isin([subjects_list])]
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, table_name, r_all)
#     subjects_list = subj_table.query("'main_condition'=!='Cognitively Normal'")["ID"].tolist()
#     df1 = df1.loc[df1['ID'].isin([subjects_list])]
#     df2 = df2.loc[df2['ID'].isin([subjects_list])]
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, table_name, r_all)
#
#     df1 = pd.read_csv("Stats_Freesurfer/aparcDKT_right.csv")
#     df2 = pd.read_csv("Stats_FastSurfer/aparcDKT_right.csv")
#
#     max_len = min(len(df1.axes[1]), len(df2.axes[1]))
#
#     subjects_list = df2.query("dx1=='Cognitively Normal'")["ID"].tolist()
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, table_name, r_all)
#
#     subjects_list = df2.query("dx1!='Cognitively Normal'")["ID"].tolist()
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, table_name, r_all)
#
#     df1 = pd.read_csv("Stats_Freesurfer/aparcDKT_left.csv")
#     df2 = pd.read_csv("Stats_FastSurfer/aparcDKT_left.csv")
#
#     max_len = min(len(df1.axes[1]), len(df2.axes[1]))
#
#     subjects_list = df2.query("dx1=='Cognitively Normal'")["ID"].tolist()
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, r_all, table_name)
#
#     subjects_list = df2.query("dx1!='Cognitively Normal'")["ID"].tolist()
#     for column_to_compare in range(2, max_len):
#         stat_test(df1, df2, column_to_compare, r_all, table_name)
#
#     save_csv(r_all)
# def save_txt(list_line):
#     file = []
#     for item in list_line:
#         file.append(item["name"])
#         file.append("\t" + item["mann_whitney"])
#         file.append("\t" + item["t_test"])
#         file.append("\n")
#     dm.write_txt(file, "old scripts/test_results.txt")
#
#
# def main_old_2():
#     base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
#
#     r_all = []
#
#     filename1 = "Stats_Freesurfer/aseg_AD.csv"
#     filename2 = "Stats_FastSurfer/aseg_AD.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     filename1 = "Stats_Freesurfer/aseg_healthy.csv"
#     filename2 = "Stats_FastSurfer/aseg_healthy.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
#
#     max_len = min(len(pd.read_csv(base_path + filename1).axes[1]), len(pd.read_csv(base_path + filename2).axes[1]))
#     for column_to_compare in range(2, max_len):
#         stat_test(base_path, filename1, filename2, column_to_compare, r_all)
#
#     save_csv(base_path,
#              r_all)
#
#
# def main_old():
#     base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
#     """
#     test order
#     aseg
#         AD left hippocampus volume
#         AD right hippocampus volume
#         healthy left hippocampus volume
#         healthy right hippocampus volume
#
#     aparc
#         AD left parahippocampal thickness
#         AD right parahippocampal thickness
#         healthy left parahippocampal thickness
#         healthy right parahippocampal thickness
#
#     """
#     r_all = []
#
#     filename1 = "Stats_Freesurfer/aseg_AD.csv"
#     filename2 = "Stats_FastSurfer/aseg_AD.csv"
#
#     column_to_compare = "Left-Hippocampus volume_mm3"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     column_to_compare = "Left-Hippocampus volume_mm3"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#     column_to_compare = "Right-Hippocampus volume_mm3"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aseg_healthy.csv"
#     filename2 = "Stats_FastSurfer/aseg_healthy.csv"
#
#     column_to_compare = "Left-Hippocampus volume_mm3"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     column_to_compare = "Right-Hippocampus volume_mm3"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
#     column_to_compare = "parahippocampal_mean_thickness_mm"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
#     column_to_compare = "parahippocampal_mean_thickness_mm"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
#     column_to_compare = "parahippocampal_mean_thickness_mm"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
#     column_to_compare = "parahippocampal_mean_thickness_mm"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
#     column_to_compare = "parahippocampal_mean_area_mm2"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
#     column_to_compare = "parahippocampal_mean_area_mm2"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
#     column_to_compare = "parahippocampal_mean_area_mm2"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
#     filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
#     column_to_compare = "parahippocampal_mean_area_mm2"
#
#     r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
#     r2 = t_test(base_path, filename1, filename2, column_to_compare)
#
#     r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
#                   "mann_whitney": r1,
#                   "t_test": r2})
#
#     # save(r_all)


if __name__ == "__main__":
    main()
