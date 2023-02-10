import data_manipulation as dm
import data_visualization as dv
import pandas as pd

# POTREI AGGIUNGERE QUI COME COSTANTI ALCUNE COSE COME IL BASE PATH ETC


"""
functions 
    get_paths_all: returns all the paths of the files that are named in a certain way in the folder
        - input -> str (base_path)
        - output -> list (paths list)
    
    filter_paths: filter according to txt file or list of subj numbers       
        - input -> list(paths list) , str or list (source as text file name or subj number list) 
        - output -> list (paths list filtered)
        
    filter_paths_from_table: filters according to all the subjects number present in an excel table (as index)      
        - input -> list (paths list), str( path to excel), *int (subj index in the table)
        - output -> list (paths list filtered)
        
    check processed: check if the subjects in the list have already been processed
        - input -> list (paths list), str (folder)
        - output -> list (paths list filtered) 
"""


def get_all_paths(base_path):
    paths_list = dm.list_files_all(dir_name, "001.mgz")

    return paths_list


def filter_paths(subj_paths_all, source):

    if source.split(".")[-1] == "txt":  # load from txt
        subj_numbers = dm.load_txt(source)

    elif source.split(".")[-1] == "xlsx":  # load from table
        table = pd.load_excel(aource)
        subj_numbers = table["subjects"].values.tolist()

    elif source.split(".")[-1] == "csv":
        table = pd.load_csv(source)
        subj_numbers = table["subjects"].values.tolist()

    elif type(source) is list:  # if list
        subj_numbers = source

    else:
        return False

    subj_paths_filtered = []
    for subj_number in subj_numbers:
        for subj_path in subj_paths_all:
            if len(subj_path.split("/")) > 3:
                match = re.split("sub-", subj_path.split("/")[-4])
                if subj_number == match[1]:
                    subj_paths_filtered.append(subj_path)

    return subj_paths_filtered


def filter_paths_from_table(table_name, destination_file, subj_idx=0):
    subj_paths_all = load_text(paths_list)
    table = pd.load_excel(table_name)
    subj_list = table["subjects"].values.tolist()

    # if filtered it filters the subjects
    if subj_idx:
        if len(subj_idx) == 2 and subj_idx[0] < subj_idx[1]:
            subj_list = subj_list[subj_idx[0], subj_idx[1]]

    subj_paths = filter_paths(subj_list, subj_paths_all)

    dm.write_txt(subj_paths, destination_file)


def check_processed(subj_paths_filtered, processed_path):
    subjs = set()

    for subj_path_filtered in subj_paths_filtered:
        subjs.add(subj_path_filtered.split("/")[-4])

    for root, dirs, files in os.walk(processed_path):
        for dir in dirs:
            if dir in subjs:
                for i, subj_path_filtered in enumerate(subj_paths_filtered):
                    if dir == subj_path_filtered.split("/")[-4]:
                        subj_paths_filtered[i] = f"subj {dir} already processed"

def main():
    save_all_images_paths("/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/", "paths_OASIS_allL.txt")
    filter_paths_from_table("OASIS_filtered.xlsx", "paths_OASIS_filtered.txt")

def main_old():
    save_all_images_paths("/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/", "paths_OASIS_allL.txt")
    filter_paths_from_table("OASIS_filtered.xlsx", "paths_OASIS_filtered.txt")
    # get_paths("subjects_AD_dementia_10_20.txt", "paths_AD_dementia_10_20.txt", "paths_AD_dementia_all.txt")


if __name__ == "__main__":
    main()


### OLD STUFF
def save_all_images_paths(dir_name, save_path):
    # list all images
    paths_list = dm.list_files_all(dir_name, "001.mgz")

    # save all the paths
    dm.write_txt(paths_list, save_path)
    return paths_list


def get_paths_txt(subject_to_select, destination_file, all_paths_file):
    """
        given a list of subjects numbers and a list of paths selects the paths of the original images of the subjects in the list
    """
    subj_numbers = load_txt(subject_to_select)
    subj_paths = []

    subj_paths_all = load_txt(all_paths_file)

    for subj_number in subj_numbers:
        for subj_path in subj_paths_all:
            if len(subj_path.split("/")) > 3:
                match = re.split("sub-", subj_path.split("/")[-4])
                if subj_number == match[1]:
                    subj_paths.append(subj_path)

    dm.write_txt(subj_paths, destination_file)
    return subj_paths


def get_paths_list(subj_numbers, subj_paths_all):
    """
        given a list of subjects numbers and a list of paths selects the paths of the original images of the subjects in the list
    """

    subj_paths = []

    for subj_number in subj_numbers:
        for subj_path in subj_paths_all:
            if len(subj_path.split("/")) > 3:
                match = re.split("sub-", subj_path.split("/")[-4])
                if subj_number == match[1]:
                    subj_paths.append(subj_path)

    return subj_paths

# table
# folder

# load paths
# filter paths with table
