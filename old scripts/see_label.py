import nibabel
import data_manipulation_helpers as dm
import data_visualization_helpers as dv
import numpy as np


def main():
    data_dict = dm.load_dict()

    labels = data_dict["r_annot"]

    label_img = dm.read_img(labels[0])

    labels = np.unique(label_img.get_fdata())

    print(labels)

if __name__ == "__main__":
    main()