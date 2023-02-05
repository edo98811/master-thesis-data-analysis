import data_manipulation as dm
import data_visualization as dv
import pandas as pd
from scipy import stats

results = []


def t_test(base_path, filename1, filename2, column_to_compare):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)
    print(base_path + filename1 + filename2)

    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]

    a = df1.loc[:, column_to_compare]
    b = df2.loc[:, column_to_compare]
    #print(a)
    #print(b)

    t_stat, p_value = stats.ttest_ind(a, b)

    # p value is the likelihood that these are the same
    print("t test")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"

    print(result)
    return result

def mann_whitney(base_path, filename1, filename2, column_to_compare):
    df1 = pd.read_csv(base_path + filename1)
    df2 = pd.read_csv(base_path + filename2)
    print(base_path + filename1 + filename2)
    
    df1 = df1[df1['subjects'].isin(df2['subjects'].tolist())]
    print(df1.head())
    print(df2.head())

    a = df1.loc[:, column_to_compare]
    b = df2.loc[:, column_to_compare]

    df1.to_csv("dataset_uniti_test.csv", index=False)
    #print(a)
    #print(b)

    t_stat, p_value = stats.mannwhitneyu(a, b)

    # p value is the likelihood that these are the same
    print("Mann Whitney")
    if p_value > 0.05:
        result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
    else:
        result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"

    print(result)
    return result

def save(list):

    file = []
    for item in list:
        file.append(item["name"])
        file.append("\t" + item["mann_whitney"])
        file.append("\t" + item["t_test"])
        file.append("\n")
    dm.write_txt(file, test_results)

if __name__ == "__main__":

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

    column_to_compare = "Left-Hippocampus volume"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    column_to_compare = "Right-Hippocampus volume"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aseg_healthy.csv"
    filename2 = "Stats_FastSurfer/aseg_healthy.csv"

    column_to_compare = "Left-Hippocampus volume"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    column_to_compare = "Right-Hippocampus volume"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
    column_to_compare = "parahippocampal mean thickness"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
    column_to_compare = "parahippocampal mean thickness"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
    column_to_compare = "parahippocampal mean thickness"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
    column_to_compare = "parahippocampal mean thickness"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_AD.csv"
    column_to_compare = "parahippocampal mean area"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_AD.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_AD.csv"
    column_to_compare = "parahippocampal mean area"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_left_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_left_healthy.csv"
    column_to_compare = "parahippocampal mean area"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})

    filename1 = "Stats_Freesurfer/aparcDKT_right_healthy.csv"
    filename2 = "Stats_FastSurfer/aparcDKT_right_healthy.csv"
    column_to_compare = "parahippocampal mean area"

    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)

    r_all.append({"name": f"{filename1.split('/')[-1]} {column_to_compare}",
                  "mann_whitney": r1,
                  "t_test": r2})