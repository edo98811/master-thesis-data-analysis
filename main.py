import FastsurferTesting as ft
import pandas as pd

ADNI_PATH = ""
OASIS_PATH = ""
BASE_PATH = ""
FREESURFER_PATH = ""


def main():
    table_oasis = ft.Table(pd.load_csv(BASE_PATH + ""))

    aseg_free = pd.load_csv(BASE_PATH + "")
    aparcL_free = pd.load_csv(BASE_PATH + "")
    aparcR_free = pd.load_csv(BASE_PATH + "")

    stats_fast_healthy = ft.Stats(table, "healthy_FAST", BASE_PATH, "'main condition'== NC")
    stats_fast_MC = ft.Stats(table, "MC_FAST", BASE_PATH, "'main condition'!= NC")

    stats_free_healthy = ft.Stats(table, "healthy_FREE", BASE_PATH, "'main condition'== NC")
    stats_free_MC = ft.Stats(table, "MC_FREE", BASE_PATH, "'main condition'!= NC", aseg=aseg_free,
                             aparcRight=aparcR_free, aparcLeft=aparcL_free)

    comp1 = ft.Comparisons(stats_free_MC, stats_fast_MC, "MC_oasis", 0.05, BASE_PATH)
    comp2 = ft.Comparisons(stats_free_healthy, stats_fast_healthy, "healthy_oasis", 0.05, BASE_PATH)
    comp1.bonferroni_correction()
    comp2.bonferroni_correction()

    comp1.violin()
    comp1.bland_altmann()

    comp2.violin()
    comp2.bland_altmann()


if __name__ == "__main__":
    main()
