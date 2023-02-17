import data_manipulation as dm
import data_visualization as dv
import pandas as pd
import re
import os
# import dropbox as dropbox_manager

# useful constants, can i modify them later?
PROCESSED_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
FREESURFER_PATH = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
# FREESURFER_PATH = "/media/neuropsycad/disk12t/VascoDiogo/ADNI"
TABLE_FILENAME = "text_and_csv_files/OASIS_filtered.csv"
FINAL_FILENAME = "text_and_csv_files/OASIS_table.csv"
FINAL_FILENAME_EXCEL = "text_and_csv_files/OASIS_table.xlsx"

"""
PROCESSED_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_Output_ADNI"
BASE_PATH = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"
FREESURFER_PATH = "/media/neuropsycad/disk12t/VascoDiogo/ADNI/"
# FREESURFER_PATH = "/media/neuropsycad/disk12t/VascoDiogo/ADNI"
TABLE_FILENAME = "text_and_csv_files/ADNI_filtered.csv"
FINAL_FILENAME = "text_and_csv_files/ADNI_table.csv"
FINAL_FILENAME_EXCEL = "text_and_csv_files/ADNI_table.xlsx"
"""


def main():
    paths = dm.list_files(FREESURFER_PATH, "001.mgz")
    # paths = dm.load_txt("")

    # dm.write_txt(paths, BASE_PATH + "test_OASIS_paths_all.txt")
    paths_on_table = filter_paths(paths, TABLE_FILENAME, subj_index=0)

    # dm.write_txt(paths_on_table, BASE_PATH + "text_and_csv_files/test_OASIS_paths_on_table.txt")
    # check_processed(paths_on_table, PROCESSED_PATH)
    #
    # dm.write_txt(paths_on_table, BASE_PATH + FINAL_FILENAME)

    df = create_table(paths_on_table)
    df.to_csv(BASE_PATH + FINAL_FILENAME, index=False)
    df.to_excel(BASE_PATH + FINAL_FILENAME_EXCEL, index=False)
    # dropbox_manager.dropbox_upload_file("", "", ".", df, FINAL_FILENAME_EXCEL)

    #df.to_excel(BASE_PATH + FINAL_FILENAME_EXCEL, index=False)
    # dropbox_manager.dropbox_upload_file("", "", ".", df, FINAL_FILENAME_EXCEL)




"""
    PART 1: creates the tables and filters the files that need to be then processed

    (get_paths_all: returns all the paths of the files that are named in a certain way in the folder
        - input -> 
            str (base_path)
        - output -> 
            list (paths list)) 
        or use dm. list_files
    
    filter_paths: filter according to txt file or list of subj numbers or excel table       
        - input -> list(paths list) , str or list (source as text file name or subj number list),  *int or str(subj index in the table)
        - output -> list (paths list filtered)
        
    check processed: check if the subjects in the list have already been processed
        - input -> 
            list (paths list)
            str (folder o check)
        - output -> list (paths list filtered) 
    
    create table 
    
    create table ADNI
        
    to use this just load a text file with all the info or call the function to lsearch for all the images from a base path 
    after to ilter it call the filter function passing as arguments , for all the functions the input subjects to check 
    are numbers not the paths 
    
    if i want to use this to select some files for exmple and check that they havent been processed yet i would wave them in a 
    txt, on for each line, then load it, and filter first according to te table, if i want to know if they exist and then according 
    to the condition if they have already been processed
"""


# filter_paths("/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/")
# filter_paths_from_table("OASIS_filtered.xlsx", "paths_OASIS_filtered.txt")
# def get_all_paths(base_path):
#     paths_list = dm.list_files(dir_name, "001.mgz")
#
#     return paths_list


# da scrivere
def count_subjs():
    pass


# filter the subjects according to a table, a list saved in a list or a simple list of subjects+
# it filters according to the subjects numbers
def filter_paths(subj_paths_all, source, subj_index=0):
    if source.split(".")[-1] == "txt":  # load from txt
        subj_numbers = dm.load_txt(BASE_PATH + source)

    elif source.split(".")[-1] == "xlsx":  # load from table
        table = pd.read_excel(BASE_PATH + source)
        if isinstance(subj_index, int):
            subj_numbers = table.iloc[:, subj_index].values.tolist()
        else:
            subj_numbers = table.loc[:, subj_index].values.tolist()

    elif source.split(".")[-1] == "csv":
        table = pd.read_csv(BASE_PATH + source)
        if isinstance(subj_index, int):
            subj_numbers = table.iloc[:, subj_index].values.tolist()
        else:
            subj_numbers = table.loc[:, subj_index].values.tolist()

    elif type(source) is list:  # if list
        subj_numbers = source

    else:
        return False

    # filter paths according to a table that contains the info of the subjects
    subj_paths_filtered = []
    for subj_number in subj_numbers:
        for subj_path in subj_paths_all:
            if len(subj_path.split("/")) > 3:
                match = re.split("sub-", subj_path.split("/")[-4])
                if subj_number == match[1]:
                    subj_paths_filtered.append(subj_path)

    return subj_paths_filtered


# checks for the subjects that have already been processed. dovrei fare la stess cosa per ADNI
def check_processed(subj_paths_filtered):
    subjs = set()

    for subj_path_filtered in subj_paths_filtered:
        subjs.add(subj_path_filtered.split("/")[-4])

    for root, dirs, files in os.walk(PROCESSED_PATH):
        for dir in dirs:
            if dir in subjs:

                for i, subj_path_filtered in enumerate(subj_paths_filtered):
                    if len(subj_path_filtered.split("/")) > 3:
                        if dir == subj_path_filtered.split("/")[-4]:
                            subj_paths_filtered[i] = f"{dir} already processed"


def create_table_ADNI(_paths_on_table):
    table = pd.read_csv(BASE_PATH + TABLE_FILENAME)

    # create the dictionary that will turn into a table
    df_dict = {
        "ID": [],
        "path": [],
        "age": [],
        "main_condition": [],
        "processed": [],
        "processed_path": []
    }

    # populates the dictionary
    for index, row in table.iterrows():
        for i, path_on_table in enumerate(_paths_on_table):
            if len(path_on_table.split("/")) > 3:
                match = re.split("sub-", path_on_table.split("/")[-4])
                if row["ID"] == match[1] and (row["_merge"] == "both" or row["_merge"] == "right_only"):
                    df_dict["ID"].append(row["ID"])
                    df_dict["path"].append(path_on_table)
                    df_dict["age"].append(row["age"])
                    df_dict["main_condition"].append(row["diagnosis"])
                    df_dict["processed"].append("no")
                    df_dict["processed_path"].append("")

    df = pd.DataFrame.from_dict(df_dict)

    subjs = set()

    # adds the paths
    # interate though all the rows to create a set of the subjects
    for i, subj_path_filtered in enumerate(df["ID"].tolist()):
        df.loc[i, "processed"] = "no"
        subjs.add("sub-" + subj_path_filtered)

    # iterate though all the directories in the processed path
    for root, dirs, files in os.walk(PROCESSED_PATH):
        for dir in dirs:
            if dir in subjs:
                # quando trova il soggetto nella crtela modifica il dataframe
                for i, subj_path_filtered in enumerate(df["ID"].tolist()):
                    if dir == "sub-" + subj_path_filtered:
                        df.loc[i, "processed"] = "yes"
                        df.loc[i, "processed_path"] = root + "/" + dir
                        break

    return df


def create_table(_paths_on_table):
    table = pd.read_csv(BASE_PATH + TABLE_FILENAME)

    # create the dictionary that will turn into a table
    df_dict = {
        "ID": [],
        "path": [],
        "age": [],
        "main_condition": [],
        "processed": [],
        "processed_path": []
    }

    # populates the dictionary
    for index, row in table.iterrows():
        for i, path_on_table in enumerate(_paths_on_table):
            if len(path_on_table.split("/")) > 3:
                match = re.split("sub-", path_on_table.split("/")[-4])
                if row["ID"] == match[1]:
                    df_dict["ID"].append(row["ID"])
                    df_dict["path"].append(path_on_table)
                    df_dict["age"].append(row["ageAtEntry"])
                    df_dict["main_condition"].append(row["dx1"])
                    df_dict["processed"].append("no")
                    df_dict["processed_path"].append("")

    df = pd.DataFrame.from_dict(df_dict)

    subjs = set()

    # adds the paths
    # interate though all the rows to create a set of the subjects
    for i, subj_path_filtered in enumerate(df["ID"].tolist()):
        df.loc[i, "processed"] = "no"
        subjs.add("sub-" + subj_path_filtered)

    # iterate though all the directories in the processed path
    for root, dirs, files in os.walk(PROCESSED_PATH):
        for dir in dirs:
            if dir in subjs:
                # quando trova il soggetto nella crtela modifica il dataframe
                for i, subj_path_filtered in enumerate(df["ID"].tolist()):
                    if dir == "sub-" + subj_path_filtered:
                        df.loc[i, "processed"] = "yes"
                        df.loc[i, "processed_path"] = root + "/" + dir
                        break

    return df
    # dm.write_txt(paths_on_table, BASE_PATH + "text_and_csv_files/test_OASIS_paths_on_table.txt")
    # check_processed(paths_on_table, PROCESSED_PATH)

    # dm.write_txt(paths_on_table, BASE_PATH + FINAL_FILENAME)


if __name__ == "__main__":
    main()

# def main_old():
#     save_all_images_paths("/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/", "paths_OASIS_allL.txt")
#     filter_paths_from_table("OASIS_filtered.xlsx", "paths_OASIS_filtered.txt")
#     # get_paths("subjects_AD_dementia_10_20.txt", "paths_AD_dementia_10_20.txt", "paths_AD_dementia_all.txt")
#
#
# def filter_paths_from_table(table_name, destination_file, subj_idx=0):
#     subj_paths_all = dm.load_txt(table_name)
#     table = pd.load_excel(table_name)
#     subj_list = table["subjects"].values.tolist()
#
#     # if filtered it filters the subjects
#     if subj_idx:
#         if len(subj_idx) == 2 and subj_idx[0] < subj_idx[1]:
#             subj_list = subj_list[subj_idx[0], subj_idx[1]]
#
#     subj_paths = filter_paths(subj_list, subj_paths_all)
#
#     dm.write_txt(subj_paths, destination_file)
#
#
# ### OLD STUFF
# def save_all_images_paths(dir_name, save_path):
#     # list all images
#     paths_list = dm.list_files_all(dir_name, "001.mgz")
#
#     # save all the paths
#     dm.write_txt(paths_list, save_path)
#     return paths_list
#
#
# def get_paths_txt(subject_to_select, destination_file, all_paths_file):
#     """
#         given a list of subjects numbers and a list of paths selects the paths of the original images of the subjects in the list
#     """
#     subj_numbers = dm.load_txt(subject_to_select)
#     subj_paths = []
#
#     subj_paths_all = dm.load_txt(all_paths_file)
#
#     for subj_number in subj_numbers:
#         for subj_path in subj_paths_all:
#             if len(subj_path.split("/")) > 3:
#                 match = re.split("sub-", subj_path.split("/")[-4])
#                 if subj_number == match[1]:
#                     subj_paths.append(subj_path)
#
#     dm.write_txt(subj_paths, destination_file)
#     return subj_paths
#
#
# def get_paths_list(subj_numbers, subj_paths_all):
#     """
#         given a list of subjects numbers and a list of paths selects the paths of the original images of the subjects in the list
#     """
#
#     subj_paths = []
#
#     for subj_number in subj_numbers:
#         for subj_path in subj_paths_all:
#             if len(subj_path.split("/")) > 3:
#                 match = re.split("sub-", subj_path.split("/")[-4])
#                 if subj_number == match[1]:
#                     subj_paths.append(subj_path)
#
#     return subj_paths

# table
# folder

# load paths
# filter paths with table
