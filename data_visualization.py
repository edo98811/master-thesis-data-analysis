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

    plt.show()


def see_data_sample(sample): #only works with image and label

    img = sample["image"]
    label = sample["label"]

    fig = plt.figure(figsize=(3, 6))

    fig.add_subplot(1, 1, 1)
    plt.imshow(img[:, :].squeeze(), cmap="gray")

    fig.add_subplot(1, 2, 2)
    plt.imshow(label[:, :].squeeze(), cmap="gray")

    plt.show()

def avg_dice(subj_data):

    all_dice_values = []
    for n in subj_data:
        if n > 0:
            all_dice_values.append(n)

    if len(all_dice_values):
        return sum(all_dice_values) / len(all_dice_values) # returns a number (avg dice for class over shubject)
    else:
        return 0



def avg_hd(subj):
    # all_dice_values = np.nonzero(np.concatenate(subj["dice_x"],subj["dice_y"],subj["dice_z"]))
    all_hd_values = np.nonzero(subj["hd_x"] + subj["hd_y"] + subj["hd_z"])
    print(all_hd_values)
    return np.average(all_hd_values)

def plot_dice(class_n, dice_scores):

    plt.bar(class_n, dice_scores)

    # set the title and labels
    plt.title('Average dice score over 10 subjects')
    plt.ylabel('Dice score')
    plt.xlabel('class')

    # show the plot
    plt.show()
def extract_data(file_path):
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            match = re.search(r'^(\d+)\s+(\w+)\s+\d+\s+\d+\s+\d+\s+\d+$', line)
            if match:
                data[match.group(1)] = match.group(2)
    return data
def plot_dice_labels(class_n, dice_scores):
    """

    :param class_n: [list of int]
    :param dice_scores: [list of float]
    :return:
    """
    # select only the dice scores and that exist and their labels
    indexes = [i for i,value in enumerate(dice_scores) if value != 0]
    dice_scores_filtered = [value for i, value in enumerate(dice_scores) if value != 0]
    class_n.pop(indexes)

    # load the freesurfer labels description
    labels = extract_data("freesurfer_labels.txt")

    # select only the labels that i need
    labels_needed =[]
    for class_number in class_n:
        labels_needed.append(labels[class_number])

    plt.bar(class_n, dice_scores_filtered)

    # set the title and labels
    plt.title('Average dice score over 10 subjects')
    plt.ylabel('Dice score')
    plt.xlabel('class')

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
