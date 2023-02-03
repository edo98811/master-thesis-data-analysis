import data_manipulation as dm
import data_visualization as dv

# basepath = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
# images_list = {"images": dm.list_files(basepath, "001.mgz")}
# # save all the useful images
# dm.write_txt(images_list["images"], "list_original_images.txt")

def main():
    #dir_name = "/media/neuropsycad/disk12t/VascoDiogo/ADNI/"
    #img_list = dm.list_files_all(dir_name, "001.mgz")
    #dm.write_txt(img_list, "ADNI_all_paths.txt")

    dm.select_paths_and_save("ADNI_subjects_10.txt", "ADNI_subjects_10_paths.txt", "ADNI_all_paths.txt")

if __name__ == "__main__":
    main()