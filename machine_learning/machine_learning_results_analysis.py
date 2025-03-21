import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy as sp
from scipy.stats import shapiro
import data_manipulation_helpers as dm

"""
questo file serve per calcolare il recap dei risultati degli algoritmi di machine learning come salvati dallo script, si carica l'excel e poi si pososno richiamare funzioni per fare i test statisticei e calcolare le metriche di riepilogo 
- init 
- recap (columns su cui farlo)
- stat_test (columns su cui farlo)
"""
BASE_PATH = "C:\\Users\\edoar\\Dropbox (Politecnico Di Torino Studenti)\\Tesi\\data_testing_ADNI\\machine_learning_0107_2"


class Data:
    def __init__(self, folder_name="..\\machine_learning_1506",
                 filenames=("\\results_FreeSurfer.xlsx", "\\results_FastSurfer.xlsx")):
        self.data1 = pd.read_excel(folder_name + filenames[0])
        self.data2 = pd.read_excel(folder_name + filenames[1])
        self.folder_name = folder_name
        self.filenames = filenames

    def stat_test(self, columns=("best_score", "MCCscore", "roc_auc")):
        res = []
        outcome = "not computed"
        result = "not computed"
        for column in columns:
            if column in self.data1.columns.tolist() and column in self.data2.columns.tolist():
                c1 = self.data1.loc[:, column]
                c2 = self.data2.loc[:, column]

                stat1, p1 = shapiro(c1)
                stat2, p2 = shapiro(c2)

                alpha = 0.05
                if p1 > alpha and p2 > alpha:
                    print('Sample looks Gaussian (fail to reject H0)')
                    stat, p_value = sp.stats.ttest_ind(c1, c2)
                    if p_value > 0.05:
                        result = f"p-value: {p_value} - null hypothesis cannot be rejected"
                        outcome = 0
                    else:
                        result = f"p-value: {p_value} - null hypothesis rejected"
                        outcome = 1

                else:
                    print('Sample does not look Gaussian (reject H0)')
                    stat, p_value = sp.stats.mannwhitneyu(c1, c2)
                    if p_value > 0.05:
                        result = f"p-value: {p_value} - null hypothesis cannot be rejected"
                        outcome = 0
                    else:
                        result = f"p-value: {p_value} - null hypothesis rejected"
                        outcome = 1

            res.append(f"{column} outcome:{outcome} - {result}")
        dm.write_txt([res], f"{self.folder_name}\\_stat_test_results.txt")

    def recap(self, columns=(
    "best_score", "best_std", "accuracy", "sensitivity", "specificity", "PPV", "NPV", "roc_auc",
    "MCCscore")):

        res1 = Data.calc_recap(self.data1, columns)
        res1.to_excel(f"{self.folder_name}\\recapFree.xlsx")
        res2 = Data.calc_recap(self.data2, columns)
        res2.to_excel(f"{self.folder_name}\\recapFast.xlsx")

    @staticmethod
    def calc_recap(data, columns):
        res = pd.DataFrame()
        for column in data.columns.tolist():
            if column in columns:
                res.loc["mean", column] = np.mean(data.loc[:, column])
                res.loc["std", column] = np.std(data.loc[:, column])

        return res


if __name__ == "__main__":
    data = Data(folder_name=BASE_PATH)
    data.recap()
    data.stat_test()
