import FastsurferTesting as ft
import pandas as pd

ADNI_PATH = ""
OASIS_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
DATA_FOLDER = "test_data/"


def main():
    table = ft.Table("OASIS TABLE", BASE_PATH, OASIS_PATH, pd.read_csv(BASE_PATH + "/text_and_csv_files/OASIS_table.csv"))

    aseg_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aseg.csv")
    aparcL_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_right.csv")
    aparcR_free = pd.read_csv(BASE_PATH + "Stats_FreeSurfer/aparcDKT_left.csv")

    stats_fast_healthy = ft.Stats("healthy_FAST", BASE_PATH, table, " main_condition!='Cognitively normal'",
                                  d_folder=DATA_FOLDER)
    stats_fast_MC = ft.Stats("MC_FAST", BASE_PATH, table, "main_condition!='Cognitively normal'", d_folder=DATA_FOLDER)

    stats_free_healthy = ft.Stats("healthy_FREE", BASE_PATH, table, "main_condition!='Cognitively normal'", BASE_PATH,
                                  DATA_FOLDER, aseg=aseg_free,
                                  aparcRight=aparcR_free, aparcLeft=aparcL_free)
    stats_free_MC = ft.Stats("MC_FREE", BASE_PATH, table, "main_condition!='Cognitively normal'", BASE_PATH,
                             DATA_FOLDER, aseg=aseg_free,
                             aparcRight=aparcR_free, aparcLeft=aparcL_free)

    comp1 = ft.Comparisons("MC_oasis", BASE_PATH, stats_free_MC, stats_fast_MC)
    comp2 = ft.Comparisons("healthy_oasis", BASE_PATH, stats_free_healthy, stats_fast_healthy)
    comp1.bonferroni_correction()
    comp2.bonferroni_correction()

    comp1.violin()
    comp1.bland_altmann()

    comp2.violin()
    comp2.bland_altmann()


if __name__ == "__main__":
    main()
