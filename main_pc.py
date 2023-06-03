import FastsurferTesting_pc as ft
import pandas as pd
import numpy as np
from comparisons_updated import SummaryPlot_updated, Comparison_updated
import os

ADNI_PATH = ""
# OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "C:\\Users\\edoar\\Dropbox (Politecnico Di Torino Studenti)\\Tesi\\data_testing_ADNI\\"
DATA_FOLDER = "to_combine_features\\"
def main_all():
    pd.options.mode.chained_assignment = None
    ft.LogWriter.clearlog()
    # np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
    # os.system("-Xfrozen_modules = off")
    table = ft.Table("ADNI_TABLE", BASE_PATH,
                     df_subj=pd.read_csv(BASE_PATH + "UPDATED_ADNI.csv"))

    table.save_csv("UPDATED_ADNI.csv")

    aseg_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg.csv")
    aparcL_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg_right.csv")
    aparcR_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg_left.csv")

    aseg_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg.csv")
    aparcL_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg_left.csv")

    aseg_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg.csv")
    aparcL_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg_right.csv")
    aparcR_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg_left.csv")

    aseg_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg.csv")
    aparcL_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg_left.csv")

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  aseg=aseg_fast_h,
                                  aparcRight=aparcR_fast_h, aparcLeft=aparcL_fast_h)
    stats_fast_MCI = ft.Stats("NotHealthy_FAST", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              aseg=aseg_fast_a,
                              aparcRight=aparcR_fast_a, aparcLeft=aparcL_fast_a)
    stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  alg="free", aseg=aseg_free_h,
                                  aparcRight=aparcR_free_h, aparcLeft=aparcL_free_h)
    stats_free_MCI = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              alg="free", aseg=aseg_free_a,
                              aparcRight=aparcR_free_a, aparcLeft=aparcL_free_a)

    #
    stats_free_MCI.normalize_stats_age()
    stats_free_healthy.normalize_stats_age()
    stats_fast_MCI.normalize_stats_age()
    stats_fast_healthy.normalize_stats_age()

    stats_free_MCI.normalize_stats_mmse()
    stats_free_healthy.normalize_stats_mmse()
    stats_fast_MCI.normalize_stats_mmse()
    stats_fast_healthy.normalize_stats_mmse()

    stats_free_MCI.clean_aparc()
    stats_free_healthy.clean_aparc()
    stats_fast_MCI.clean_aparc()
    stats_fast_healthy.clean_aparc()

    # stats_free_MCI.save_stats_normalized()
    # stats_free_healthy.save_stats_normalized()
    # stats_fast_MCI.save_stats_normalized()
    # stats_fast_healthy.save_stats_normalized()
    # #
    # summary1 = SummaryPlot_updated("FreeSurfer", BASE_PATH, [stats_free_healthy, stats_free_MCI], d_folder=DATA_FOLDER)
    # # summary1.scatter_plot_aseg_mmse()
    # summary1.scatter_plot_aseg_normalized_linear_regression()
    # # summary1.scatter_plot_aseg_normalized_huber_regression()
    # # summary1.scatter_plot_aseg_normalized_regression_confidence()
    # summary2 = SummaryPlot_updated("FastSurfer", BASE_PATH, [stats_fast_healthy, stats_fast_MCI], d_folder=DATA_FOLDER)
    # # summary2.scatter_plot_aseg_mmse()
    # summary2.scatter_plot_aseg_normalized_linear_regression()
    #
    # # summary2.scatter_plot_aseg_normalized_huber_regression()
    # # summary2.scatter_plot_aseg_normalized_regression_confidence()
    # summary3 = SummaryPlot_updated("Healthy", BASE_PATH, [stats_fast_healthy, stats_free_healthy], d_folder=DATA_FOLDER)
    # # summary3.scatter_plot_aseg_mmse()
    # summary3.scatter_plot_aseg_normalized_linear_regression()
    #
    # # summary3.scatter_plot_aseg_normalized_huber_regression()
    # # summary3.scatter_plot_aseg_normalized_regression_confidence()
    # summary4 = SummaryPlot_updated("Pathologic", BASE_PATH, [stats_fast_MCI, stats_free_MCI], d_folder=DATA_FOLDER)
    # # summary4.scatter_plot_aseg_mmse()
    # summary4.scatter_plot_aseg_normalized_linear_regression()
    #
    # summary4.scatter_plot_aseg_normalized_huber_regression()
    # summary4.scatter_plot_aseg_normalized_regression_confidence()

    comp1 = Comparison_updated("Pathologic", BASE_PATH, stats_free_MCI, stats_fast_MCI, d_folder=DATA_FOLDER)
    comp2 = Comparison_updated("Healthy", BASE_PATH, stats_free_healthy, stats_fast_healthy, d_folder=DATA_FOLDER)
    comp3 = Comparison_updated("FastSurfer", BASE_PATH, stats_fast_healthy, stats_fast_MCI, d_folder=DATA_FOLDER, categories=("Healthy", "Pathologic"))
    comp4 = Comparison_updated("FreeSurfer", BASE_PATH, stats_free_healthy, stats_free_MCI, d_folder=DATA_FOLDER, categories=("Healthy", "Pathologic"))
    # comp5 = Comparison_updated("FastSurfer", BASE_PATH, stats_fast_healthy, stats_fast_MCI, d_folder=DATA_FOLDER,
    #                            categories=("Healthy", "Pathologic"))
    # comp6 = Comparison_updated("FreeSurfer", BASE_PATH, stats_free_healthy, stats_free_MCI, d_folder=DATA_FOLDER,
    #                            categories=("Healthy", "Pathologic"))

    comp1.stat_test(match=True)
    comp2.stat_test(match=True)
    comp3.stat_test()
    comp4.stat_test()

    comp1.bonferroni_correction()
    comp2.bonferroni_correction()
    comp3.bonferroni_correction()
    comp4.bonferroni_correction()
    comp1.save_data()
    comp2.save_data()
    comp3.save_data()
    comp4.save_data()

    #comp1.violin()
    #comp1.bland_altmann()
    #
    #comp2.violin()
    #comp2.bland_altmann()
    #
    # comp3.violin()
    #comp3.bland_altmann()
    #
    # comp4.violin()
    #comp4.bland_altmann()

def main():
    pd.options.mode.chained_assignment = None
    ft.LogWriter.clearlog()
    # np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)
    # os.system("-Xfrozen_modules = off")
    table = ft.Table("ADNI_TABLE", BASE_PATH,
                     df_subj=pd.read_csv(BASE_PATH + "UPDATED_ADNI.csv"))

    table.save_csv("UPDATED_ADNI.csv")

    aseg_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg.csv")
    aparcL_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg_right.csv")
    aparcR_free_h = pd.read_csv(BASE_PATH + "stats\\healthy_FREE_stats\\aseg_left.csv")

    aseg_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg.csv")
    aparcL_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_h = pd.read_csv(BASE_PATH + "stats\\healthy_FAST_stats\\aseg_left.csv")

    aseg_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg.csv")
    aparcL_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg_right.csv")
    aparcR_free_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FREE_stats\\aseg_left.csv")

    aseg_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg.csv")
    aparcL_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg_right.csv")
    aparcR_fast_a = pd.read_csv(BASE_PATH + "stats\\NotHealthy_FAST_stats\\aseg_left.csv")

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  aseg=aseg_fast_h,
                                  aparcRight=aparcR_fast_h, aparcLeft=aparcL_fast_h)
    stats_fast_MCI = ft.Stats("NotHealthy_FAST", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              aseg=aseg_fast_a,
                              aparcRight=aparcR_fast_a, aparcLeft=aparcL_fast_a)
    stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", d_folder=DATA_FOLDER,
                                  alg="free", aseg=aseg_free_h,
                                  aparcRight=aparcR_free_h, aparcLeft=aparcL_free_h)
    stats_free_MCI = ft.Stats("NotHealthy_FREE", BASE_PATH, table, "main_condition!='NL'", d_folder=DATA_FOLDER,
                              alg="free", aseg=aseg_free_a,
                              aparcRight=aparcR_free_a, aparcLeft=aparcL_free_a)
    #
    stats_free_MCI.normalize_stats_age()
    stats_free_healthy.normalize_stats_age()
    stats_fast_MCI.normalize_stats_age()
    stats_fast_healthy.normalize_stats_age()

    stats_free_MCI.normalize_stats_mmse()
    stats_free_healthy.normalize_stats_mmse()
    stats_fast_MCI.normalize_stats_mmse()
    stats_fast_healthy.normalize_stats_mmse()

    stats_free_MCI.clean_aparc()
    stats_free_healthy.clean_aparc()
    stats_fast_MCI.clean_aparc()
    stats_fast_healthy.clean_aparc()

    stats_free_MCI.save_stats_normalized()
    stats_free_healthy.save_stats_normalized()
    stats_fast_MCI.save_stats_normalized()
    stats_fast_healthy.save_stats_normalized()
    #
    # summary1 = SummaryPlot_updated("FreeSurfer", BASE_PATH, [stats_free_healthy, stats_free_MCI], d_folder=DATA_FOLDER)
    # # summary1.scatter_plot_aseg_mmse()
    # summary1.scatter_plot_aseg_normalized_linear_regression(
    #     c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3", "3rd-Ventricle_volume_mm3",
    #                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3", "Right-Amygdala_volume_mm3",
    #                "Right-Accumbens-area_volume_mm3"])
    # # summary1.scatter_plot_aseg_normalized_huber_regression()
    # # summary1.scatter_plot_aseg_normalized_regression_confidence()
    # summary2 = SummaryPlot_updated("FastSurfer", BASE_PATH, [stats_fast_healthy, stats_fast_MCI], d_folder=DATA_FOLDER)
    # # summary2.scatter_plot_aseg_mmse()
    # summary2.scatter_plot_aseg_normalized_linear_regression(
    #     c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3", "3rd-Ventricle_volume_mm3",
    #                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3", "Right-Amygdala_volume_mm3",
    #                "Right-Accumbens-area_volume_mm3"])
    #
    # # summary2.scatter_plot_aseg_normalized_huber_regression()
    # # summary2.scatter_plot_aseg_normalized_regression_confidence()
    # summary3 = SummaryPlot_updated("Healthy", BASE_PATH, [stats_fast_healthy, stats_free_healthy], d_folder=DATA_FOLDER)
    # # summary3.scatter_plot_aseg_mmse()
    # summary3.scatter_plot_aseg_normalized_linear_regression(
    #     c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3", "3rd-Ventricle_volume_mm3",
    #                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3", "Right-Amygdala_volume_mm3",
    #                "Right-Accumbens-area_volume_mm3"])
    #
    # # summary3.scatter_plot_aseg_normalized_huber_regression()
    # # summary3.scatter_plot_aseg_normalized_regression_confidence()
    # summary4 = SummaryPlot_updated("Pathologic", BASE_PATH, [stats_fast_MCI, stats_free_MCI], d_folder=DATA_FOLDER)
    # # summary4.scatter_plot_aseg_mmse()
    # summary4.scatter_plot_aseg_normalized_linear_regression(
    #     c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3", "3rd-Ventricle_volume_mm3",
    #                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3", "Right-Amygdala_volume_mm3",
    #                "Right-Accumbens-area_volume_mm3"])

    # summary4.scatter_plot_aseg_normalized_huber_regression()
    # summary4.scatter_plot_aseg_normalized_regression_confidence()

    comp1 = Comparison_updated("Pathologic", BASE_PATH, stats_free_MCI, stats_fast_MCI, d_folder=DATA_FOLDER)
    comp2 = Comparison_updated("Healthy", BASE_PATH, stats_free_healthy, stats_fast_healthy, d_folder=DATA_FOLDER)
    comp3 = Comparison_updated("FastSurfer", BASE_PATH, stats_fast_healthy, stats_fast_MCI, d_folder=DATA_FOLDER, categories=("Healthy", "Pathologic"))
    comp4 = Comparison_updated("FreeSurfer", BASE_PATH, stats_free_healthy, stats_free_MCI, d_folder=DATA_FOLDER, categories=("Healthy", "Pathologic"))

    comp1.stat_test(match=True, c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
                             "3rd-Ventricle_volume_mm3",
                             "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
                             "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
                             "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
                             "Right-Amygdala_volume_mm3",
                             "Right-Accumbens-area_volume_mm3"])
    comp2.stat_test(match=True, c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
                             "3rd-Ventricle_volume_mm3",
                             "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
                             "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
                             "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
                             "Right-Amygdala_volume_mm3",
                             "Right-Accumbens-area_volume_mm3"])
    comp3.stat_test(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
                             "3rd-Ventricle_volume_mm3",
                             "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
                             "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
                             "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
                             "Right-Amygdala_volume_mm3",
                             "Right-Accumbens-area_volume_mm3"])
    comp4.stat_test(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
                             "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
                             "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
                             "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
                             "3rd-Ventricle_volume_mm3",
                             "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
                             "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
                             "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
                             "Right-Amygdala_volume_mm3",
                             "Right-Accumbens-area_volume_mm3"])

    comp1.bonferroni_correction()
    comp2.bonferroni_correction()
    comp3.bonferroni_correction()
    comp4.bonferroni_correction()
    comp1.save_data()
    comp2.save_data()
    comp3.save_data()
    comp4.save_data()

    # comp1.violin(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    #                         "3rd-Ventricle_volume_mm3",
    #                         "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                         "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                         "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    #                         "Right-Amygdala_volume_mm3",
    #                         "Right-Accumbens-area_volume_mm3"])
    # # comp1.bland_altmann(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    # #                                "3rd-Ventricle_volume_mm3",
    # #                                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3",
    # #                                "Left-Amygdala_volume_mm3",
    # #                                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    # #                                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    # #                                "Right-Amygdala_volume_mm3",
    # #                                "Right-Accumbens-area_volume_mm3"])
    # #
    # comp2.violin(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    #                         "3rd-Ventricle_volume_mm3",
    #                         "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                         "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                         "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    #                         "Right-Amygdala_volume_mm3",
    #                         "Right-Accumbens-area_volume_mm3"])
    # # comp2.bland_altmann(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    # #                                "3rd-Ventricle_volume_mm3",
    # #                                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3",
    # #                                "Left-Amygdala_volume_mm3",
    # #                                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    # #                                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    # #                                "Right-Amygdala_volume_mm3",
    # #                                "Right-Accumbens-area_volume_mm3"])
    # #
    # comp3.violin(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    #                         "3rd-Ventricle_volume_mm3",
    #                         "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                         "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                         "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    #                         "Right-Amygdala_volume_mm3",
    #                         "Right-Accumbens-area_volume_mm3"])
    # # comp3.bland_altmann(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    # #                                "3rd-Ventricle_volume_mm3",
    # #                                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3",
    # #                                "Left-Amygdala_volume_mm3",
    # #                                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    # #                                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    # #                                "Right-Amygdala_volume_mm3",
    # #                                "Right-Accumbens-area_volume_mm3"])
    # #
    # comp4.violin(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    #                         "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    #                         "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    #                         "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    #                         "3rd-Ventricle_volume_mm3",
    #                         "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3", "Left-Amygdala_volume_mm3",
    #                         "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    #                         "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    #                         "Right-Amygdala_volume_mm3",
    #                         "Right-Accumbens-area_volume_mm3"])
    # # comp4.bland_altmann(c_to_keep=["middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "middletemporal_mean_thickness_mm", "middletemporal_mean_area_mm2",
    # #                                "parahippocampal_mean_thickness_mm", "parahippocampal_mean_area_mm2",
    # #                                "superiortemporal_mean_thickness_mm", "superiortemporal_mean_area_mm2",
    # #                                "Left-Lateral-Ventricle_volume_mm3", "Left-Inf-Lat-Vent_volume_mm3",
    # #                                "3rd-Ventricle_volume_mm3",
    # #                                "4th-Ventricle_volume_mm3", "Left-Hippocampus_volume_mm3",
    # #                                "Left-Amygdala_volume_mm3",
    # #                                "Left-Accumbens-area_volume_mm3", "Right-Lateral-Ventricle_volume_mm3",
    # #                                "Right-Inf-Lat-Vent_volume_mm3", "Right-Hippocampus_volume_mm3",
    # #                                "Right-Amygdala_volume_mm3",
    # #                                "Right-Accumbens-area_volume_mm3"])



if __name__ == "__main__":
    main_all()
