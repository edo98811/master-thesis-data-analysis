import matplotlib.pyplot as plt
import torch

def see_random_slice(img):
    torch.manual_seed(42)
    fig = plt.figure(figsize=(9, 9))
    rows, cols = 4, 4
    for i in range(1, rows * cols + 1):
        random_idx = torch.randint(0, img.shape[0], size=[1]).item() #transforms in normal python int
        fig.add_subplot(rows, cols, i)
        plt.imshow(img[random_idx,:,:].squeeze(), cmap="gray")
        plt.title(f"slice: {random_idx}")
        plt.axis(False);


def see_data_sample(sample): #only works with image and label

    img = sample["image"]
    label = sample["label"]

    fig = plt.figure(figsize=(3, 6))

    fig.add_subplot(1, 1, 1)
    plt.imshow(img[:, :].squeeze(), cmap="gray")

    # TODO: controllare se è ncessario squeeze
    fig.add_subplot(1, 2, 2)
    plt.imshow(label[:, :].squeeze(), cmap="gray")

    plt.show()