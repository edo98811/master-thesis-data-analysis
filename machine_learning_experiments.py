import machine_learning_models as ml
import FastsurferTesting_pc as ft
import comparisons_updated as cu


import FastsurferTesting_pc as ft
import pandas as pd
import numpy as np
from comparisons_updated import SummaryPlot_updated, Comparison_updated

ADNI_PATH = ""
# OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "C:\\Users\\edoar\\Dropbox (Politecnico Di Torino Studenti)\\Tesi\\data_testing_ADNI\\"
DATA_FOLDER = "test_data_ADNI_0205r\\"


def main():
    ft.LogWriter.clearlog()
    # np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)

    table = ft.Table("ADNI_TABLE", BASE_PATH,
                     df_subj=pd.read_csv(BASE_PATH + "UPDATED_ADNI.csv"))

    table.save_csv("UPDATED_ADNI.csv")

    aseg_free_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FREE_stats\\aseg.csv")
    aparcL_free_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FREE_stats\\aseg_right.csv")
    aparcR_free_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FREE_stats\\aseg_left.csv")

    aseg_fast_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FAST_stats\\aseg.csv")
    aparcL_fast_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_h = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\healthy_FAST_stats\\aseg_left.csv")

    aseg_free_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FREE_stats\\aseg.csv")
    aparcL_free_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FREE_stats\\aseg_right.csv")
    aparcR_free_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FREE_stats\\aseg_left.csv")

    aseg_fast_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FAST_stats\\aseg.csv")
    aparcL_fast_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_a = pd.read_csv(BASE_PATH + "data_testing_ADNI_workstation\\NotHealthy_FAST_stats\\aseg_left.csv")

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  aseg=aseg_fast_h,
                                  aparcRight=aparcR_fast_h, aparcLeft=aparcL_fast_h)
    stats_fast_MCI = ft.Stats("NotHsealthy_FAST", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              aseg=aseg_fast_a,
                              aparcRight=aparcR_fast_a, aparcLeft=aparcL_fast_a)
    stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  alg="free", aseg=aseg_free_h,
                                  aparcRight=aparcR_free_h, aparcLeft=aparcL_free_h)
    stats_free_MCI = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              alg="free", aseg=aseg_free_a,
                              aparcRight=aparcR_free_a, aparcLeft=aparcL_free_a)

    stats_free_MCI.normalize_stats_age()
    stats_free_healthy.normalize_stats_age()
    stats_fast_MCI.normalize_stats_age()
    stats_fast_healthy.normalize_stats_age()

    stats_free_MCI.clean_aparc()
    stats_free_healthy.clean_aparc()
    stats_fast_MCI.clean_aparc()
    stats_fast_healthy.clean_aparc()

    model = ml.Models_Binary([stats_fast_MCI, stats_fast_healthy], BASE_PATH)
    model.logistic_regression()
    # print(model.X)
    # model.X.to_excel(BASE_PATH + "dataset.xlsx")
    # print(model.X_new.shape)

    print("ciao")

if __name__ == "__main__":
    main()
