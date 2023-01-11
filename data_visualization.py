import matplotlib.pyplot as plt
import torch
import numpy as np
def see_random_slice(img):
    torch.manual_seed(42)
    fig = plt.figure(figsize=(9, 9))
    rows, cols = 4, 4
    for i in range(1, rows * cols + 1):
        random_idx = torch.randint(0, img.shape[0], size=[1]).item() #transforms in normal python int
        fig.add_subplot(rows, cols, i)
        plt.imshow(img[random_idx,:,:].squeeze(), cmap="gray")
        plt.title(f"slice: {random_idx}")
        plt.axis(False)


def see_data_sample(sample): #only works with image and label

    img = sample["image"]
    label = sample["label"]

    fig = plt.figure(figsize=(3, 6))

    fig.add_subplot(1, 1, 1)
    plt.imshow(img[:, :].squeeze(), cmap="gray")

    fig.add_subplot(1, 2, 2)
    plt.imshow(label[:, :].squeeze(), cmap="gray")

    plt.show()

def avg_dice(subj):
    # all_dice_values = np.nonzero(np.concatenate(subj["dice_x"],subj["dice_y"],subj["dice_z"]))
    all_dice_values = np.nonzero(subj["dice_x"] + subj["dice_y"] + subj["dice_z"])
    print(all_dice_values)
    return np.average(all_dice_values, axis=None)

def avg_hd(subj):
    # all_dice_values = np.nonzero(np.concatenate(subj["dice_x"],subj["dice_y"],subj["dice_z"]))
    all_hd_values = np.nonzero(subj["hd_x"] + subj["hd_y"] + subj["hd_z"])
    print(all_hd_values)
    return np.average(all_hd_values)

def plot_dice(subjects, dice_scores):

    plt.bar(subjects, dice_scores)

    # set the title and labels
    plt.title('Average dice score over 10 subjects')
    plt.ylabel('Dice score')
    plt.xlabel('Subject')

    # show the plot
    plt.show()

    
def plot_hd(subjects, dice_scores):

    plt.bar(subjects, dice_scores)

    # set the title and labels
    plt.title('Average dice score over 10 subjects')
    plt.ylabel('Dice score')
    plt.xlabel('Subject')

    # show the plot
    plt.show()
