import pandas as pd
from pandas.api.types import CategoricalDtype


def HelenaOASIS(path):

    df = pd.read_excel(path)
    df = df.drop_duplicates(subset=df.columns[1])

    # rename the "Subject" column to "ID"
    df = df.rename(columns={"Subject": "ID"})

    # set the "ID" column as the index of the dataframe
    df.set_index("ID", inplace=True)
    print(df.head())

    # create a table for rows where the fourth column is "healthy"
    healthy_df = df[df.loc[:, "dx1"] == "Cognitively normal"]

    # create a table for rows where the fourth column is not "healthy"
    others_df = df[df.loc[:, "dx1"] != "Cognitively normal"]
    # others_df = filtered_df[filtered_df.iloc[:, 8] == "AD Dementia"]




    # with pd.ExcelWriter(
    #         r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\OASIS_filtered.xlsx") as writer:
    #     healthy_df.to_excel(writer, sheet_name='Healthy')
    #     others_df.to_excel(writer, sheet_name='Not Healthy')

    healthy_df.to_csv(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\OASIS_filtered_healthy.csv")
    others_df.to_csv(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\OASIS_filtered_not_healthy.csv")

def VascoADNI(path1, path2):
    df1 = pd.read_excel(path1, index_col=None, usecols='A:J')
    df2 = pd.read_excel(path2, index_col=None)

    df1.rename(columns={"Subject ID": "ID"}, inplace=True)
    # df1.index.name = "ID"
    # df2['ID'] = df2['year'].astype(int)
    print(df1.head())
    print(df2.head())

    df = pd.merge(df1, df2, how="outer", on="ID", indicator=True)

    df.set_index("ID", inplace=True)
    merge_type = CategoricalDtype(['both', 'left_only', 'right_only'], ordered=True)
    df['_merge'] = df['_merge'].astype(merge_type)
    df.sort_values(by='_merge', inplace=True)

    # df.drop(columns=['age', 'sex'], inplace=True)

    print(df.head())

    # with pd.ExcelWriter(
    #         r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\ADNI_merged.xlsx") as writer:
    #     df.to_excel(writer)

    df.to_csv(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\ADNI_filtered.csv")


if __name__ == "__main__":
    # VascoADNI(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\PopulationCharacteristics.xlsx",
    #           r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\subjs_demographic_cognitive_data.xlsx")

    HelenaOASIS(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\subjs_diagnosis.xlsx")