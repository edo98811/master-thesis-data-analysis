import FastsurferTesting_workstation as ft
import comparisons_updated as ftu
import pandas as pd
import numpy as np

ADNI_PATH = ""
DATASET_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/MPRAGE_SPGR_imgs_Alzheimer"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
DATA_FOLDER = "Portuguese_Processed/"
PROCESSED_PATH = ""


def main():
    ft.LogWriter.clearlog()

    table = ft.Table("ADNI_TABLE", BASE_PATH, dataset_path=DATASET_PATH, p_path=PROCESSED_PATH)

    table.save_csv("Portuguese.csv")

    # aseg_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aseg.csv")
    # aparcL_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_right.csv")
    # aparcR_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_left.csv")

    # stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, " main_condition=='NL'")
    # stats_fast_MCI = ft.Stats("NotHealthy_FAST", BASE_PATH, table, "main_condition!='NL'")
    # stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", alg="free")
    # stats_free_MCI = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "main_condition!='NL'", alg="free")

    # stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, "")
    # stats_fast_MCI = ft.Stats("NotHealthy_FAST", BASE_PATH, table, "")
    # stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "", alg="free")
    # stats_free_MCI = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "", alg="free")

    # stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", aseg=aseg_free,
    #                               aparcRight=aparcR_free, aparcLeft=aparcL_free)
    # stats_free_MC = ft.Stats("MC_FREE", BASE_PATH, table, "main_condition!='NL'", aseg=aseg_free,
    #                          aparcRight=aparcR_free, aparcLeft=aparcL_free)

    # stats_fast_healthy.save_stats_files()
    # stats_fast_MCI.save_stats_files()
    # stats_free_healthy.save_stats_files()
    # stats_free_MCI.save_stats_files()
    #
    # comp1 = ftu.Comparison_updated("NotHealthy_ADNI", BASE_PATH, stats_free_MCI, stats_fast_MCI, d_folder=DATA_FOLDER)
    # comp2 = ftu.Comparison_updated("healthy_ADNI", BASE_PATH, stats_free_healthy, stats_fast_healthy, d_folder=DATA_FOLDER)
    # comp1.stat_test()
    # comp2.stat_test()
    #
    # #
    # comp1.bonferroni_correction()
    # comp2.bonferroni_correction()
    # comp1.save_data()
    # comp2.save_data()
    #
    # comp2.violin()
    # comp2.bland_altmann()
    #
    # comp2.violin()
    # comp2.bland_altmann()
    #
    # summary1 = ftu.SummaryPlot_updated("summary", BASE_PATH, [stats_free_MCI, stats_fast_MCI, stats_free_healthy,
    #                                                  stats_fast_healthy], d_folder=DATA_FOLDER)
    # summary1.comparison_plot_line()
    # ft.LogWriter()


if __name__ == "__main__":
    main()
