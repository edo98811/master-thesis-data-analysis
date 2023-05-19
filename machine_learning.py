import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import sklearn.metrics as metrics
import sklearn.feature_selection as feature_selection
import pandas as pd
import os
import data_manipulation as dm
import imblearn as im
import comparisons_updated as cu
import FastsurferTesting_pc as ft
import numpy as np
import missingno as msno

"""
idee 
    togliere referenze a self 
    fare in modo che i model sano ritornati e che quindi sia tutto modulare per poterne usare molti 
    salvare risultati in excel

"""


class Models_Binary:
    def __init__(self, data, base_path, data_path="\\machine_learning"):

        self.X_normalized = None
        self.X_feature_selected = None
        if len(data) == 2:
            self.data = data
        else:
            raise Exception("wrong number of class inputs (only binary classification)")
        self.base_path = base_path

        self.data_path = base_path + data_path
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        self.X, self.Y = self._dataset_preparation()
        ft.LogWriter.log("dataset object created")

    @staticmethod
    def _select_dataset(d, stats_object):

        if d == "aseg":
            dataframe_selected = stats_object.df_stats_aseg
            subj_lists = stats_object.df_stats_aseg["ID"].tolist()
            columns = set(stats_object.df_stats_aseg.columns.tolist())
        elif d == "aparcR":
            dataframe_selected = stats_object.df_stats_aparcL
            subj_lists = stats_object.df_stats_aparcL["ID"].tolist()
            columns = set(stats_object.df_stats_aparcL.columns.tolist())
        elif d == "aparcL":
            dataframe_selected = stats_object.df_stats_aparcL
            subj_lists = stats_object.df_stats_aparcL["ID"].tolist()
            columns = set(stats_object.df_stats_aparcL.columns.tolist())
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
    def _drop_nan(X):
        cols_to_drop = []
        for name in X.columns.tolist():
            if X.loc[:, name].isnull().values.any():
                # X.loc[:, column] = X.loc[:, column].fillna(0)
                cols_to_drop.append(name)
                # drop column
        X.drop(columns=cols_to_drop, inplace=True)
        return X

    def save_dataset(self, X, y=None, filename="dataset.xlsx"):

        ft.LogWriter.log("dataset saved")
        if y is None:
            df = X
        else:
            df = pd.concat([y, X], axis=1)

        df.to_excel(f"{self.data_path}{filename}")
        dm.write_txt(df.columns.tolist(), f"{self.data_path}features.txt")

    def _dataset_preparation(self, data=("aparcL_cleaned", "aparcR_cleaned", "aseg_normalized"),
                             columns_to_exclude=("mmse")):

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
                        df_class.drop(column, inplace=True)

                df_class["class"] = i

            if 'df_class' in locals():
                df = pd.concat([df, df_class], axis=0)
            else:
                raise Exception("dataset could not be created")

        df = df.sample(frac=1)

        # df.to_excel(f"{self.base_path}dataset.xlsx")

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

    @staticmethod
    def feature_selection(X, y, features=None, method=0):
        X_feature_selected = None
        Models_Binary._drop_nan(X)
        if features is None:
            if method == 0:
                X_feature_selected = X
            if method == 1:
                X_feature_selected = feature_selection.SelectKBest(score_func=feature_selection.f_classif,
                                                                   k=10).fit_transform(
                    X, y)
        else:
            X_feature_selected = X[X.columns.intersection(features)]

        return X_feature_selected

    @staticmethod
    def _set_splitting(X, y, test=0.2, method="under"):
        """
        :param X:
        :param y:
        :param test:
        :param method: "under", "over", "balance_same_seed"
        :return:
        """

        if method == "under":
            under_sampler = im.under_sampling.RandomUnderSampler(random_state=42)
            X_balanced, y_balanced = under_sampler.fit_resample(X, y)
            Models_Binary.check_balance(y_balanced)

            X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=test, random_state=0)

        elif method == "over":
            under_sampler = im.over_sampling.RandomOverSampler(random_state=42)
            X_balanced, y_balanced = under_sampler.fit_resample(X, y)
            Models_Binary.check_balance(y_balanced)

            X_train, X_test, y_train, y_test = train_test_split(X_balanced, y_balanced, test_size=test, random_state=0)

        elif method == "no":
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=0)
        elif method == "balance_same_seed":
            np.random.seed(42)

            data = np.hstack((X, np.expand_dims(y.to_numpy(), axis=1)))
            class1 = data[data[:, -1] == 1, :]
            class2 = data[data[:, -1] == 0, :]
            n = int(np.ceil((1 - test) * min(len(class1), len(class2))))

            train1 = np.random.permutation(range(len(class1)))[:n]
            train2 = np.random.permutation(range(len(class2)))[:n]

            test1 = np.random.permutation(range(len(class1)))[n + 1:]
            test2 = np.random.permutation(range(len(class2)))[n + 1:]

            train = np.concatenate(([class1[train1, :], class2[train2, :]]), axis=0)
            test = np.concatenate(([class1[test1, :], class2[test2, :]]), axis=0)
            np.random.shuffle(train)
            np.random.shuffle(test)

            Models_Binary.check_balance(train)
            Models_Binary.check_balance(test)
            y_train = train[:, -1]
            X_train = train[:, :-2]
            y_test = test[:, -1]
            X_test = test[:, :-2]
        else:
            return None

        return X_train, X_test, y_train, y_test

    @staticmethod
    def check_balance(y):
        # byclass = self.X.groupby(by="class").count()
        # ft.LogWriter.log(f"{byclass}")
        ft.LogWriter.log(f"{len(y['class'==1])}")
        ft.LogWriter.log(f"{len(y['class' == 0])}")

    @staticmethod
    def normalize_features(X, method="minmax"):
        if method == "standard":
            X_normalized = sklearn.preprocessing.StandardScaler().fit_transform(X)
        elif method == "minmax":
            X_normalized = sklearn.preprocessing.MinMaxScaler().fit_transform(X)
        elif method == "other":
            X_normalized = sklearn.preprocessing.MinMaxScaler().fit_transform(X)
        else:
            return None

        return X_normalized

    @staticmethod
    def train_model(X_train, y_train, model_type):
        if model_type == "logistic":
            model = LogisticRegression().fit(X_train, y_train)
        elif model_type == "svm":
            model = SVC().fit(X_train, y_train)
        else:
            raise Exception("invalid model type")

        return model

    @staticmethod
    def test_model(X_test, model):
        return model.predict(X_test)

    @staticmethod
    def metrics(y_test, y_pred, index):

        results_dict = dict()

        results_dict["text"] = metrics.classification_report(y_test, y_pred)
        results_dict["accuracy"] = metrics.accuracy_score(y_test, y_pred)
        results_dict["precision"] = metrics.precision_score(y_test, y_pred)
        results_dict["recall"] = metrics.recall_score(y_test, y_pred)
        results_dict["balanced_accuracy"] = metrics.balanced_accuracy_score(y_test, y_pred)
        results_dict["confusion_matrix"] = metrics.confusion_matrix(y_test, y_pred)

        results_series = pd.Series(results_dict)
        results_series.name = index

        return results_series

    def classify(self, filename, features=None, feature_selection_method=None, normalization=("minmax",),
                 model_type=("logistic", "svm"), setbalance=("balance_same_seed",), n_iter=2):
        """

        :param features:
        :param feature_selection_method:
        :param normalization:
        :param model_type:
        :param setbalance:
        :param n_iter:
        :return:
        """
        res = pd.DataFrame()

        X_selected = self.feature_selection(self.X, self.Y, features=features, method=feature_selection_method)
        for n_ in normalization:
            X_normalized = self.normalize_features(X_selected, method=n_)
            for sb_ in setbalance:
                X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y, method=sb_)

                for m_ in model_type:
                    for i in range(n_iter):
                        index = f"{m_}_{sb_}_{n_}_{i}"

                        model = Models_Binary.train_model(X_train, y_train, m_)
                        y_pred = Models_Binary.test_model(X_test, model)
                        res = pd.concat([res, Models_Binary.metrics(y_test, y_pred, index)], axis=1)

        res.to_excel(self.data_path + filename)

    # def medial_temporal_lobe_atrophy_score(self, features=None):
    #
    #     if features is None:
    #         features = []
    #
    #     a = features[0]
    #     b = features[1]
    #     c = features[3]
    #
    # def HAV_atrophy_score(self):
    #     model = 1
    #
    # def feature_tests(self):
    #     pass
    # def logistic_regression(self, features=None, normalization="minmax", model="logistc", setbalance="balance_same_seed"):
    #
    #     X_fs = self.feature_selection(self.X, self.Y, features=features)
    #     X_normalized = self.normalize_features(X_fs)
    #
    #     X_train, X_test, y_train, y_test = self._set_splitting(X_normalized, self.Y)
    #
    #     model_log = LogisticRegression().fit(X_train, y_train)
    #     y_pred_log = model_log.predict(X_test)
    #
    #     # %% md
    #     # 16. Compare the end results by their accuracy
    #     # %%
    #     acc_log = accuracy_score(y_test, y_pred_log)
    #     print(f"accuracy under sampling: {acc_log}")
    #     del X_train, X_test, y_train, y_test
    #
    #     X_train, X_test, y_train, y_test = self._set_splitting(self.X_normalized, self.Y, balance="over")
    #     model_log = LogisticRegression().fit(X_train, y_train)
    #     y_pred_log = model_log.predict(X_test)
    #
    #     # %% md
    #     # 16. Compare the end results by their accuracy
    #     # %%
    #     acc_log = accuracy_score(y_test, y_pred_log)
    #     print(f"accuracy over sampling: {acc_log}")
