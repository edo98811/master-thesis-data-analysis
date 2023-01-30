import data_manipulation as dm
import data_visualization as dv

# basepath = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
# images_list = {"images": dm.list_files(basepath, "001.mgz")}
# # save all the useful images
# dm.write_txt(images_list["images"], "list_original_images.txt")

def main():
    dm.select_paths_and_save("AD_dementia_subjects.txt", "AD_dementia_subjects_paths.txt")



if __name__ == "__main__":
    main()