import pandas as pd
import os

def main():
    path = r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\subjs_diagnosis.xlsx"
    assert os.path.isfile(path)
    df = pd.read_excel(path)

    # unique_values = df.iloc[:, 1].unique()

    filtered_df = df.drop_duplicates(subset=df.columns[1])

    # create a table for rows where the fourth column is "healthy"
    healthy_df = filtered_df[filtered_df.iloc[:, 8] == "Cognitively normal"]

    # create a table for rows where the fourth column is not "healthy"
    others_df = filtered_df[filtered_df.iloc[:, 8] != "Cognitively normal"]
    # others_df = filtered_df[filtered_df.iloc[:, 8] == "AD Dementia"]

    with pd.ExcelWriter(r"C:\Users\edoar\OneDrive - CLOUDEA S.R.L\Polito Materiale\BIOMEDICA\Tesi\subj_diagnosis_filtered.xlsx") as writer:
        healthy_df.to_excel(writer, sheet_name='Healthy')
        others_df.to_excel(writer, sheet_name='Not Healthy')

if __name__ == "__main__":
    main()