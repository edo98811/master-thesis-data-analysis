import machine_learning as ml
import FastsurferTesting_pc as ft
import comparisons_updated as cu
import pandas as pd
import numpy as np
import data_manipulation as dm
from comparisons_updated import SummaryPlot_updated, Comparison_updated

ADNI_PATH = ""
# OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "C:\\Users\\edoar\\Dropbox (Politecnico Di Torino Studenti)\\Tesi\\data_testing_ADNI\\"
DATA_FOLDER = "machine_learning\\"


def main():
    ft.LogWriter.clearlog()
    # np.warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)

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

    res = pd.DataFrame()
    param_grid = {9: {
        'n_estimators': [100, 200, 300],  # Number of trees in the forest
        'criterion': ['gini', 'entropy'],  # Splitting criterion
        'max_depth': [None, 5, 10],  # Maximum depth of the tree
        'min_samples_split': [2, 5, 10],  # Minimum number of samples required to split an internal node
        'min_samples_leaf': [1, 2, 4],  # Minimum number of samples required to be at a leaf node
        'bootstrap': [True, False]  # Whether bootstrap samples are used when building trees
    }}
    for nc, pt, name in zip([stats_free_MCI, stats_fast_MCI], [stats_free_healthy, stats_fast_healthy],
                            ["free", "fast"]):
        model = ml.Models_Binary([nc, pt], BASE_PATH, data_path=DATA_FOLDER)
        # model.save_dataset(model.X)
        for i in range(5):
            f = dm.load_txt(BASE_PATH + f"\\fs\\selected_features{i + 1}.txt")
            res = pd.concat([res, model.classify(f"{i + 1}_{name}", features=f, params=param_grid)], axis=0)

    res.to_excel(BASE_PATH + DATA_FOLDER + "results_kfold2.xlsx")
    # # for freesurfer
    # model = ml.Models_Binary([stats_free_MCI, stats_free_healthy], BASE_PATH, data_path=DATA_FOLDER)
    # # model.save_dataset(model.X)
    # for i in range(5):
    #     f = dm.load_txt(BASE_PATH + f"\\fs\\selected_features{i+1}.txt")
    #     res = pd.concat([res, model.classify(f"{i+1}", features=f)], axis=0)
    #
    # # for fastsurfer
    # model = ml.Models_Binary([stats_fast_MCI, stats_fast_healthy], BASE_PATH, data_path=DATA_FOLDER)
    # # model.save_dataset(model.X)
    #
    # for i in range(5):
    #     f = dm.load_txt(BASE_PATH + f"\\fs\\selected_features{i+1}.txt")
    #     res = pd.concat([res, model.classify(f"{i+1}", features=f)], axis=0)

    # indexes = {"experiment1":[(-1, "Left-Lateral-Ventricle_volume_mm3"), (-1, "Left-Inf-Lat-Vent_volume_mm3"),
    #            (-1, "Right-Inf-Lat-Vent_volume_mm3"), (-1, "3rd-Ventricle_volume_mm3"),
    #            (-1, "4th-Ventricle_volume_mm3"), (-1, "Right-Lateral-Ventricle_volume_mm3"),
    #            (1, "Right-Amygdala_volume_mm3"), (1, "Left-Amygdala_volume_mm3"), (1, "Left-Hippocampus_volume_mm3"),
    #            (1, "Right-Hippocampus_volume_mm3"), (1, "Left-Accumbens-area_volume_mm3"),
    #            (1, "Right-Accumbens-area_volume_mm3")],
    #            "experiment2":[(1, "Right-Amygdala_volume_mm3"), (1, "Left-Amygdala_volume_mm3"), (1, "Left-Hippocampus_volume_mm3"),
    #            (1, "Right-Hippocampus_volume_mm3"), (1, "Left-Accumbens-area_volume_mm3"),
    #            (1, "Right-Accumbens-area_volume_mm3")]
    #            }
    # model = ml.Models_Binary([stats_fast_MCI, stats_fast_healthy], BASE_PATH, data_path=DATA_FOLDER)
    # model.scores("scoresFastSurfer.xlsx", indexes)
    # model = ml.Models_Binary([stats_free_MCI, stats_free_healthy], BASE_PATH, data_path=DATA_FOLDER)
    # model.scores("scores_FreeSurfer.xlsx", indexes)


if __name__ == "__main__":
    main()
