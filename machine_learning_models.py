import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import sklearn.feature_selection as feature_selection
import pandas as pd
import os
import comparisons_updated as cu
import FastsurferTesting_pc as ft
import numpy as np
import missingno as msno



class Models_Binary:
    def __init__(self, data, base_path, data_path="\\machine_learning"):

        if len(data) == 2:
            self.data = data
        else:
            raise "wrong number of class inputs (only binary classification)"
        self.base_path = base_path

        self.data_path = base_path + data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        self.X, self.Y = self._dataset_preparation()

    def _select_dataset(self, d, stats_object):

        if d == "aseg":
                dataframe_selected = stats_object.df_stats_aseg
                subj_lists = stats_object.df_stats_aseg["ID"].tolist()
                columns = set(stats_object.df_stats_aseg.columns.tolist())
        elif d == "aparcR":
                dataframe_selected = stats_object.df_stats_aparcL
                subj_lists = stats_object.df_stats_aparcL["ID"].tolist()
                columns = set(stats_object.df_stats_aparcL.columns.tolist())
        elif d == "aparcL":
                dataframe_selected = stats_object.df_stats_aparcR
                subj_lists = stats_object.df_stats_aparcR["ID"].tolist()
                columns = set(stats_object.df_stats_aparcR.columns.tolist())
        elif d == "aseg_normalized":
                dataframe_selected = stats_object.aseg_normalized
                subj_lists = stats_object.aseg_normalized.index.values.tolist()
                columns = set(stats_object.aseg_normalized.columns.tolist())
        elif d == "aseg_normalized_mmse":
                dataframe_selected = stats_object.aseg_normalized_mmse
                subj_lists = stats_object.aseg_normalized_mmse.index.values.tolist()
                columns = set(stats_object.aseg_normalized_mmse.columns.tolist())
        elif d == "aparcL_cleaned":
                dataframe_selected = stats_object.aparcL_cleaned
                subj_lists = stats_object.aparcL_cleaned.index.values.tolist()
                columns = set(stats_object.aparcL_cleaned.columns.tolist())
        elif d == "aparcR_cleaned":
                dataframe_selected = stats_object.aparcR_cleaned
                subj_lists = stats_object.aparcR_cleaned.index.values.tolist()
                columns = set(stats_object.aparcR_cleaned.columns.tolist())
        else:
            return None, None, None

        columns_set = set(columns)

        return dataframe_selected, subj_lists, columns_set
    @staticmethod
    def drop_nan(X):
        cols_to_drop = []
        for name in X.columns.tolist():
            if X.loc[:, name].isnull().values.any():
                # X.loc[:, column] = X.loc[:, column].fillna(0)
                cols_to_drop.append(name)
                # drop column
        X.drop(columns=cols_to_drop, inplace=True)
        return X

    def _dataset_preparation(self, data=("aparcL_cleaned", "aparcR_cleaned", "aseg_normalized"), columns_to_exclude = ("mmse")):

        df = pd.DataFrame()
        for i, stats_object in enumerate(self.data):
            df_class = pd.DataFrame()
            subjects_ID = set()
            columns_all = set()

            for d in data:
                dataframe_selected, subj_lists, columns_set = self._select_dataset(d, stats_object)
                # devo essere sicuro che gli indici coincidano tra tutti i dataframe

                df_class = pd.concat([df_class, dataframe_selected], axis=1)
                subjects_ID = subjects_ID.union(subj_lists)
                columns_all = columns_all.union(columns_set)

                for column in columns_all:
                    if column in columns_to_exclude:
                            df_class.drop(column, inplace =True)

                df_class["class"] = i

            if 'df_class' in locals():
                df = pd.concat([df, df_class], axis=0)
            else:
                raise "dataset could not be created"

        df = df.sample(frac=1)

        #df.to_excel(f"{self.base_path}dataset.xlsx")

        Y = df.loc[:, "class"].copy(deep=True)
        X = df.drop(columns=["class"]).copy(deep=True)


        return X, Y
        """
        :param decode:
        :param dataframe_selected:
        :return:
        """
        """
        idee
            un altra idea è unsare una lista di due da unire per creare il dataset, la lista contiene in una quelly sani 
            e in una quelli dell'altro dataset
            - potrei usare due queries per selezionare i soggetti che sono da considerare healthy e quelli che non lo sono 
        dafare 
            - filtrare i soggetti usando la query, devo aggiungere 0 e 1 alla fine del dataset per ogni soggetto 
            - eliminare le colonne inutili 
            - unificare tutte le features
            - dividere il dataframe
            - salvare dataset x
            - salvare dataset y 
        """

    def anova_feature_selection(self):
        # msno.matrix(self.X)
        self.drop_nan(self.X)
        X_new = feature_selection.SelectKBest(score_func=feature_selection.f_classif, k=10).fit_transform(self.X, self.Y)

        return X_new

    def feature_selection(self, list=[""]):
        # msno.matrix(self.X)
        self.drop_nan(self.X)
        X_new = feature_selection.SelectKBest(score_func=feature_selection.f_classif, k=10).fit_transform(self.X, self.Y)

        return X_new

    def _set_splitting(self, X, y, test=0.2):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=0)

        return X_train, X_test, y_train, y_test

    def logistic_regression(self, features):

        if not os.path.isfile(self.data_path + "dataset_complete.xlsx"):
            self.X.to_excel(self.data_path + "dataset_complete.xlsx")

        self.X_new = self.feature_selection(features)

        X_train, X_test, y_train, y_test = self._set_splitting(self.X_new, self.Y)
        # print(self.X_new)


        model_log = LogisticRegression().fit(X_train, y_train)
        y_pred_log = model_log.predict(X_test)

        # %% md
        # 16. Compare the end results by their accuracy
        # %%
        acc_log = accuracy_score(y_test, y_pred_log)
        print(f"accuracy: {acc_log}")


