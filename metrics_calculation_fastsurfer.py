import data_manipulation as dm
import data_visualization as dv
import metrics as m
from os.path import dirname
import os
import numpy as np

def main():
    #images_list_freesurfer, images_list_fastsurfer = images_paths()
    metrics = {
        # "image":{
        #     "dice": list,
        #     "hd": list
        #     ...
        #
        #      },
        # "image2":
    }
    images = dm.load_dict("aseg_paths.json")
    images_list_freesurfer = images["free"]
    images_list_fastsurfer = images["fast"]

    for image_path_free, image_path_fast in zip(images_list_fastsurfer, images_list_freesurfer):
        subj = ''.join(image_path_free).split('/')[-3]
        image_fast = dm.read_img(image_path_fast).dataobj
        image_free = dm.read_img(image_path_free).dataobj

        metrics.update(metrics_calculation(image_fast, image_free, subj))
        # dv.see_random_slice(image_free)
        # dv.see_random_slice(image_fast)
        print(f"subj:{subj} done")
    # dv.see_random_slice(image_fast)
    dm.write_dict(metrics, "metrics.json")

def metrics_calculation(image_fast, image_free, subj):

    dice_z = []
    hd_z = []
    dice_y = []
    hd_y = []
    dice_x = []
    hd_x = []

    n_classes = np.amax(image_free)
    # dv.see_random_slice(image_fast)
    print(image_fast.shape)

    # maybe here it's better to use arrays and not lists
    # for slice_n in range(image_fast.shape[2]):
    # dice_z.append((m.dice_coefficient(image_fast[:,:,slice_n], image_free[:,:,slice_n])))
    # hd_z.append((m.hausdorff_distance(image_fast[:,:,slice_n], image_free[:,:,slice_n])))
    # print(f"slice {slice_n} done")
    # print("dim 2 done")

    # for slice_n in range(image_fast.shape[1]):
    # dice_y.append((m.dice_coefficient(image_fast[:,slice_n,:], image_free[:,slice_n,:])))
    # hd_y.append((m.hausdorff_distance(image_fast[:,slice_n,:], image_free[:,slice_n,:])))
    # print("dim 0 done")

    for slice_n in range(image_fast.shape[0]):
        dice_x.append(m.dice_multiclass(image_fast[slice_n, :, :], image_free[slice_n, :, :],n_classes))
        # hd_x.append((m.hausdorff_distance(image_fast[slice_n,:,:], image_free[slice_n,:,:])))
        print(f"slice {slice_n} done, dice scores: {dice_x[-1]} ")
    print("dim 1 done")

    return {subj: {"dice_z": dice_z, "hd_z": hd_z,
                   "dice_x": dice_x, "hd_x": hd_x,
                   "dice_y": dice_y, "hd_y": hd_y}}

# rendere questa parte di script più generale (farci funzione)
def images_paths():
    # save all the useful images paths, should work with any path
    basepath_fastsurfer = "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/FastSurfer_output/"
    images_list_fastsurfer_tmp = dm.list_files(basepath_fastsurfer, "aseg.mgz")
    basepath_freesurfer = "/media/neuropsycad/disk12t/VascoDiogo/OASIS/FS7/"
    images_list_freesurfer_tmp = dm.list_files(basepath_freesurfer, "aseg.mgz")

    images_list_fastsurfer = []
    images_list_freesurfer = []
    for image_path_free in images_list_freesurfer_tmp:
        for image_path_fast in images_list_fastsurfer_tmp:
            if ''.join(image_path_fast).split('/')[-3] == ''.join(image_path_free).split('/')[-3]:
                images_list_freesurfer.append(image_path_free)
                images_list_fastsurfer.append(image_path_fast)

    del images_list_freesurfer_tmp, images_list_fastsurfer_tmp
    # after this i should only have the paths to the images i have processed

    dm.write_dict({"free": images_list_freesurfer, "fast": images_list_fastsurfer}, "aseg_paths.json")

    print("saved")
    return images_list_freesurfer, images_list_fastsurfer

if __name__ == "__main__":
    main()