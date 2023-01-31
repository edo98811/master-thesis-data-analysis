import data_manipulation as dm
import data_visualization as dv
import pandas as pd
from scipy import stats

if __name__ == "__main__":
    base_path = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/Stats/"
    filename1 = "aparcDKT_right_healthy.csv"
    filename2 = "aparcDKT_right_AD.csv"
    column_to_compare = 4

    table1 = pd.read_csv(base_path + filename1)
    table2 = pd.read_csv(base_path + filename2)

    a = table1.iloc[:, column_to_compare]
    b = table2.iloc[:, column_to_compare]
    print(a)

    t_stat, p_value = stats.ttest_ind(a, b)

    if p_value > 0.05:
        print ("null hipothesys cannot be rejected")
    else
        print ("null hipothesys rejected")