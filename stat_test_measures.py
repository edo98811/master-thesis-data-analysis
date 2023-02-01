import data_manipulation as dm
import data_visualization as dv
import pandas as pd
from scipy import stats

def t_test(base_path, filename1, filename2, column_to_compare):
    table1 = pd.read_csv(base_path + filename1)
    table2 = pd.read_csv(base_path + filename2)

    a = table1.loc[:, column_to_compare]
    b = table2.loc[:, column_to_compare]
    print(a)
    print(b)

    t_stat, p_value = stats.ttest_ind(a, b)

    # p value is the likelihood that these are the same
    print("t test")
    if p_value > 0.05:
        print(f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal")
    else:
        print(f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal")

def mann_whitney(base_path, filename1, filename2, column_to_compare):
    table1 = pd.read_csv(base_path + filename1)
    table2 = pd.read_csv(base_path + filename2)

    a = table1.loc[:, column_to_compare]
    b = table2.loc[:, column_to_compare]
    print(a)
    print(b)

    t_stat, p_value = stats.mannwhitneyu(a, b)

    # p value is the likelihood that these are the same
    print("Mann Whitney")
    if p_value > 0.05:
        print(f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal")
    else:
        print(f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal")

if __name__ == "__main__":

    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
    filename1 = "Stats_Freesurfer/aseg_AD.csv"
    filename2 = "Stats_FastSurfer/aseg_AD.csv"
    column_to_compare = "Left-Hippocampus volume"

    mann_whitney(base_path, filename1, filename2, column_to_compare)
    t_test(base_path, filename1, filename2, column_to_compare)
