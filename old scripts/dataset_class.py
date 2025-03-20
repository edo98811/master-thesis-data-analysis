from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from data_manipulation_helpers import load_dict, read_img
from torch.utils.data import Dataset, DataLoader
from math import floor
from torchvision import transforms, utils

#  controllare il tipo di dati

class MriDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, data_file_path, dim, split,  transform=None):
        """
        Args:
            data_file_path
            dim
            split - array (begin, end)
            transform
        """
        self.data_file_path = data_file_path
        self.data_plane = dim

        files = load_dict(data_file_path)

        #: migliorare questa cosa
        self.label_list = files["r_annot"][floor(split[0]*len(files["r_annot"])):floor(split[1]*len(files["r_annot"]))]
        self.dataset_list = files["r_img"][floor(split[0]*len(files["r_annot"])):floor(split[1]*len(files["r_annot"]))]
        self.img_dim = read_img(self.dataset_list[0]).shape[dim] # poi questo adrà modificato
        self.transform = transform

    def __len__(self):
        return len(self.dataset_list)*self.img_dim

    def __getitem__(self, idx):

        img_n = floor(idx / self.img_dim)
        img_idx =  idx - (img_n * self.img_dim)

        print(img_idx)
        print(img_n)


        #
        # aggiungere un controllo che i tipi di dati siano corretti, e aggiungere modo piu veloce di fare questo controllo
        vol_img = read_img(self.dataset_list[img_n]).dataobj
        vol_label = read_img(self.label_list[img_n]).dataobj

        if self.data_plane == 0:
            img = vol_img[img_idx,:,:]
            label = vol_label[img_idx,:,:]
        elif self.data_plane == 1:
            img = vol_img[ :, img_idx, :]
            label = vol_label[ :, img_idx, :]
        elif self.data_plane == 2:
            img = vol_img[:,: ,img_idx]
            label = vol_label[:,: ,img_idx]

        sample = {'image': img, 'label': label}

        if self.transform:
            sample = self.transform(sample)

        return sample


        # if torch.is_tensor(idx):
        #     idx = idx.tolist()

        # img_name = os.path.join(self.root_dir,
        #                         self.landmarks_frame.iloc[idx, 0])
        # image = io.imread(img_name)
        # landmarks = self.landmarks_frame.iloc[idx, 1:]
        # landmarks = np.array([landmarks])
        # landmarks = landmarks.astype('float').reshape(-1, 2)
        # sample = {'image': image, 'landmarks': landmarks}

        # return sample