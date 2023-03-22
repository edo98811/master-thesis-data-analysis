import FastsurferTesting as ft
import pandas as pd
import numpy as np

ADNI_PATH = ""
OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
DATA_FOLDER = "test_data/"


def main():
    ft.LogWriter.clearlog()


    table = ft.Table("ADNI_TABLE", BASE_PATH, OASIS_PATH,
                     pd.read_csv(BASE_PATH + "/text_and_csv_files/ADNI_table.csv"))


    table.save_csv("UPDATED_ADNI.csv")

    # aseg_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aseg.csv")
    # aparcL_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_right.csv")
    # aparcR_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_left.csv")

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, " main_condition=='NL'")
    stats_fast_MC = ft.Stats("NotHealthy_FAST", BASE_PATH, table, "main_condition!='NL'")
    stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", alg="free")
    stats_free_MC = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "main_condition!='NL'", alg="free")

    # stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", aseg=aseg_free,
    #                               aparcRight=aparcR_free, aparcLeft=aparcL_free)
    # stats_free_MC = ft.Stats("MC_FREE", BASE_PATH, table, "main_condition!='NL'", aseg=aseg_free,
    #                          aparcRight=aparcR_free, aparcLeft=aparcL_free)

    stats_fast_healthy.save_stats_files()
    stats_fast_MC.save_stats_files()
    stats_free_healthy.save_stats_files()
    stats_free_MC.save_stats_files()

    comp1 = ft.Comparisons("NotHealthy_ADNI", BASE_PATH, stats_free_MC, stats_fast_MC)
    comp2 = ft.Comparisons("healthy_ADNI", BASE_PATH, stats_free_healthy, stats_fast_healthy)
    comp1.stat_test()
    comp2.stat_test()
    comp1.save_data()
    comp2.save_data()

    comp1.bonferroni_correction()
    comp2.bonferroni_correction()

    comp2.violin(data="aseg")
    comp2.violin(data="aparcL")
    comp2.violin(data="aparcR")
    comp2.bland_altmann(data="aseg")
    comp2.bland_altmann(data="aparcL")
    comp2.bland_altmann(data="aparcR")

    comp2.violin(data="aseg")
    comp2.violin(data="aparcL")
    comp2.violin(data="aparcR")
    comp2.bland_altmann(data="aseg")
    comp2.bland_altmann(data="aparcL")
    comp2.bland_altmann(data="aparcR")

    summary1 = ft.SummaryPlot("summary", BASE_PATH, [stats_free_MC, stats_fast_MC, stats_free_healthy,
                                                     stats_fast_healthy])
    summary1.comparison_plot(data="aseg")
    summary1.comparison_plot(data="aparcL")
    summary1.comparison_plot(data="aparcR")

    # ft.LogWriter()


if __name__ == "__main__":
    main()
