import data_manipulation as dm
import data_visualization as dv
import pandas as pd

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

def main():
    save_all_images_paths("/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/", "paths_OASIS_allL.txt")
    filter_paths_from_table("OASIS_filtered.xlsx", "paths_OASIS_filtered.txt")
    #get_paths("subjects_AD_dementia_10_20.txt", "paths_AD_dementia_10_20.txt", "paths_AD_dementia_all.txt")

def filter_paths_from_table(table_name, destination_file, subj_idx=0):

    subj_paths_all = load_text(paths_list)
    table = pd.load_excel(table_name)
    subj_list = table["subjects"].values.tolist()

    # if filtered it filters the subjects
    if subj_idx:
        if len(subj_idx) == 2 and subj_idx[0] < subj_idx[1]:
            subj_list = subj_list[subj_idx[0], subj_idx[1]]

    subj_paths = get_paths_list(subj_list, subj_paths_all)
    dm.write_txt(subj_paths, destination_file)


if __name__ == "__main__":
    main()

# table
# folder

# load paths
# filter paths with table
