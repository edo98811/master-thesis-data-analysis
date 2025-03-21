import matplotlib.pyplot as plt
import torch
import numpy as np
import re
import data_manipulation_helpers as dm

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
    """
    :param subj_data: list of values (for one dice)
    :return: mean
    """

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
            match = re.search(r'^(\d+)\s+([\w-]+)\s+\d+\s+\d+\s+\d+\s+\d+$', line)
            if match:
                data[match.group(1)] = match.group(2)
    return data

def plot_dice_labels(class_n, dice_scores):
    """

    :param class_n: [list of int]
    :param dice_scores: [list of float] or [list of lists of float]
    :return:
    """


    # calculates the average for every element of a list (average of all the first elements, second, etc)
    dice_scores_tmp = []
    if isinstance(dice_scores, list):
        for i in range(len(dice_scores[0])): # itera lungo la lunghezza della lista
            dice_score_tmp = [dice_scores[j][i] for j in range(len(dice_scores))] #prende l'elemento i da tutte le liste (j)
            dice_scores_tmp.append(avg_dice(dice_score_tmp)) # calcola la media

        del dice_scores
        dice_scores = dice_scores_tmp
        del dice_scores_tmp

    # select only the dice scores and that exist and their labels
    class_n_filtered = []
    dice_scores_filtered = []

    for i,value in enumerate(dice_scores):
        if value != 0:
            class_n_filtered.append(class_n[i])
            dice_scores_filtered.append(dice_scores[i])

    # indexes = [i for i,value in enumerate(dice_scores) if value == 0]
    # print(dice_scores)
    # print(indexes)
    # print(len(indexes))
    #
    # for index in indexes:
    #     class_n.pop(index)
    #
    # print(class_n)
    # del indexes,index
    #
    # dice_scores_filtered = [value for i, value in enumerate(dice_scores) if value != 0]


    # load the freesurfer labels description
    #labels = extract_data("freesurfer_labels.txt")
    #dm.write_dict(labels,"freesurfer_labels.json")
    labels = dm.load_dict("old scripts/freesurfer_labels.json")

    # select only the labels that i need
    labels_needed =[]
    for class_number in class_n_filtered:
        if str(class_number) in labels.keys():
            labels_needed.append(labels[str(class_number)])


    # x axis
    x_axis =[i for i in range(len(class_n_filtered))]
    x_ticks_list = list(map(str, class_n_filtered))

    # plot
    plt.bar(x_axis, dice_scores_filtered)

    # set the title and labels
    plt.title('Average dice score over 10 subjects')
    plt.ylabel('Dice score')
    plt.xlabel('class')

    # set the region values
    plt.xticks(x_axis,labels_needed,rotation='60', ha='right')

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
