#da adattare

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