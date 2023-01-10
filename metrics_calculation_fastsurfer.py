import data_manipulation as dm
import data_visualization as dv
import metrics as m
from os.path import dirname
import numpy as np

def main():
    # save all the useful images paths, should work with any path
    basepath_fastsurfer = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_output/"
    images_list_fastsurfer = dm.list_files(basepath_fastsurfer, "aseg.mgz")
    basepath_freesurfer = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/sub-OAS31172/"
    images_list_freesurfer = dm.list_files(basepath_freesurfer, "aseg.mgz")

    dm.write_dict({"free": images_list_freesurfer, "fast": images_list_fastsurfer}, "aseg_paths.json")

    metrics = {
        # "image":{
        #     "dice": list,
        #     "hd": list
        #     ...
        #
        #      },
        # "image2":
    }


    for image_path_free, image_path_fast in zip(images_list_fastsurfer, images_list_freesurfer):

        image_fast = dm.read_img(image_path_fast).dataobj
        image_free = dm.read_img(image_path_free).dataobj

        metrics.update(metrics_calculation(image_fast, image_free, image_path_free.split("/")[-2]))
        dv.see_random_slice(image_free)
        dv.see_random_slice(image_fast)

    dm.write_dict(metrics,"metrics.json")

def metrics_calculation(image_fast, image_free, subj):
    dice_z = []
    hd_z = []
    dice_y = []
    hd_y = []
    dice_x = []
    hd_x = []

    # maybe here it's better to use arrays and not lists
    for slice_n in range(image_fast.shape[2]):
        dice_z.append((m.dice_coefficient(image_fast[:,:,slice_n], image_free[:,:,slice_n])))
        #hd_z.append((m.hausdorff_distance(image_fast[:,:,slice_n], image_free[:,:,slice_n])))

    for slice_n in range(image_fast.shape[1]):
        dice_y.append((m.dice_coefficient(image_fast[:,slice_n,:], image_free[:,slice_n,:])))
        #hd_y.append((m.hausdorff_distance(image_fast[:,slice_n,:], image_free[:,slice_n,:])))

    for slice_n in range(image_fast.shape[0]):
        dice_x.append((m.dice_coefficient(image_fast[slice_n,:,:], image_free[slice_n,:,:])))
        #hd_x.append((m.hausdorff_distance(image_fast[slice_n,:,:], image_free[slice_n,:,:])))

    # prova
    # add a way to find the name of the image
    return {subj:{"dice_z": dice_z, "hd_z": hd_z,
    "dice_x": dice_x, "hd_x": hd_x,
    "dice_y": dice_y, "hd_y": hd_y}}

if __name__ == "__main__":
    main()