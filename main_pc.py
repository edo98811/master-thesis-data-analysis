import FastsurferTesting_pc as ft
import pandas as pd
import numpy as np
from comparisons_updated import SummaryPlot_updated, Comparison_updated

ADNI_PATH = ""
# OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "C:\\Users\\edoar\\Dropbox (Politecnico Di Torino Studenti)\\Tesi\\data_testing_ADNI\\"
DATA_FOLDER = "test_data_ADNI_dopo_incontro\\"


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

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, " main_condition=='NL'", d_folder=DATA_FOLDER,
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

    stats_free_MCI.save_stats_with_age()
    stats_free_healthy.save_stats_with_age()
    stats_fast_MCI.save_stats_with_age()
    stats_fast_healthy.save_stats_with_age()

    summary1 = SummaryPlot_updated("summary_free", BASE_PATH, [stats_free_healthy], d_folder=DATA_FOLDER)
    summary1.scatter_plot_aseg_with_ages()
    # stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition=='NL'", aseg=aseg_free,
    #                               aparcRight=aparcR_free, aparcLeft=aparcL_free)
    # stats_free_MCI = ft.Stats("MC_FREE", BASE_PATH, table, "main_condition!='NL'", aseg=aseg_free,
    #                          aparcRight=aparcR_free, aparcLeft=aparcL_free)

    # stats_fast_healthy.save_stats_files()
    # stats_fast_MCI.save_stats_files()
    # stats_free_healthy.save_stats_files()
    # stats_free_MCI.save_stats_files()

    # comp1 = Comparison_updated("NotHealthy_ADNI", BASE_PATH, stats_free_MCI, stats_fast_MCI, d_folder=DATA_FOLDER)
    # comp2 = Comparison_updated("healthy_ADNI", BASE_PATH, stats_free_healthy, stats_fast_healthy, d_folder=DATA_FOLDER)
    # comp1.stat_test()
    # comp2.stat_test()
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

    # summary1 = SummaryPlot_updated("summary_not_healthy", BASE_PATH, [stats_free_MCI, stats_fast_MCI],
    #                                d_folder=DATA_FOLDER)
    # summary1.model_fit()

    # comp1 = Comparison_updated("free_ADNI", BASE_PATH, stats_free_MCI, stats_free_healthy, d_folder=DATA_FOLDER,
    #                            categories=("MCI", "healthy"))
    # comp2 = Comparison_updated("fast_ADNI", BASE_PATH, stats_fast_MCI, stats_fast_healthy, d_folder=DATA_FOLDER,
    #                            categories=("MCI", "healthy"))
    #
    # comp1.violin(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                        'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                        'Right-Caudate_volume_mm3', 'Right-Caudate_volume_mm3'])
    #
    # comp1.violin(data=["aparcL"], c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # comp1.violin(data=["aparcR"], c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    #
    # comp2.violin(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                        'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                        'Right-Caudate_volume_mm3', 'Right-Caudate_volume_mm3'])
    #
    # comp2.violin(data=["aparcL"], c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # comp2.violin(data=["aparcR"], c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])

    # comp2.violin()
    # comp2.bland_altmann()

    # summary1 = SummaryPlot_updated("summary_free", BASE_PATH, [stats_free_healthy, stats_free_MCI
    #                                                            ], d_folder=DATA_FOLDER)
    # summary1 = SummaryPlot_updated("summary_free", BASE_PATH, [stats_free_healthy
    #                                                            ], d_folder=DATA_FOLDER)
    """
    totale plots 
    
    comparison 2
        6 aseg
        2 aparcR
        2 aparcL
        
            3 images

    comparison 1
        6 aseg
        2 aparcR
        2 aparcL
        
            3 images
    
    total -> 6 images     
    """
    # summary1.model_fit(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                              'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                              'Right-Caudate_volume_mm3', 'Left-Caudate_volume_mm3'])
    # summary1.model_fit(data=["aparcL"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary1.model_fit(data=["aparcR"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary1.comparison_plot_line(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                              'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                              'Right-Caudate_volume_mm3', 'Left-Caudate_volume_mm3'])
    # summary1.comparison_plot_line(data=["aparcL"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary1.comparison_plot_line(data=["aparcR"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary2 = SummaryPlot_updated("summary_fast", BASE_PATH, [stats_fast_healthy, stats_fast_MCI]
    #                                , d_folder=DATA_FOLDER)
    # # summary2 = SummaryPlot_updated("summary_fast", BASE_PATH, [stats_free_MCI]
    # #                                , d_folder=DATA_FOLDER)
    #
    # summary2.model_fit(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                              'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                              'Right-Caudate_volume_mm3', 'Left-Caudate_volume_mm3'])
    # summary2.model_fit(data=["aparcL"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary2.model_fit(data=["aparcR"],
    #
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    #
    # summary2.comparison_plot_line(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                              'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                              'Right-Caudate_volume_mm3', 'Left-Caudate_volume_mm3'])
    # summary2.comparison_plot_line(data=["aparcL"],
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary2.comparison_plot_line(data=["aparcR"],
    #
    #                    c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary3 = SummaryPlot_updated("summary_fast", BASE_PATH, [stats_fast_healthy]
    #                                , d_folder=DATA_FOLDER)
    # summary3.model_fit(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                                         'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                                         'Right-Caudate_volume_mm3', 'Right-Caudate_volume_mm3'])
    # summary3.model_fit(data=["aparcL"],
    #                               c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary3.model_fit(data=["aparcR"],
    #                               c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    #
    # summary4 = SummaryPlot_updated("summary_fast", BASE_PATH, [stats_fast_MCI]
    #                                , d_folder=DATA_FOLDER)
    # summary4.model_fit(data=["aseg"], c_to_keep=['Right-Hippocampus_volume_mm3', 'Left-Amygdala_volume_mm3',
    #                                                         'Left-Hippocampus_volume_mm3', 'Right-Amygdala_volume_mm3',
    #                                                         'Right-Caudate_volume_mm3', 'Right-Caudate_volume_mm3'])
    # summary4.model_fit(data=["aparcL"],
    #                               c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # summary4.model_fit(data=["aparcR"],
    #                               c_to_keep=["entorhinal_mean_area_mm2", "entorhinal_mean_thickness_mm"])
    # ft.LogWriter()


if __name__ == "__main__":
    main()
