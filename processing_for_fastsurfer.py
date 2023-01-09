import data_manipulation as dm
import data_visualization as dv

def main():
    basepath = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"

    # save all the useful images
    images_list = dm.list_files(basepath, "001")
    dm.save_dict(images_list,"list_original_images.json")


if __name__ == "__main__":
    main()