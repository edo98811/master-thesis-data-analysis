from scipy.spatial.distance import euclidean
import numpy as np


def hausdorff_distance(mask1, mask2):
    # Convert the masks to sets of points
    points1 = set((i, j) for i in range(mask1.shape[0]) for j in range(mask1.shape[1]) if mask1[i, j])
    points2 = set((i, j) for i in range(mask2.shape[0]) for j in range(mask2.shape[1]) if mask2[i, j])

    # If one of the sets is empty, the Hausdorff distance is infinity
    if not points1 or not points2:
        return float('inf')

    # Calculate the Hausdorff distance
    return max(
        max(min(euclidean(p, q) for q in points2) for p in points1),
        max(min(euclidean(p, q) for p in points1) for q in points2)
    )


# da fare per maschere non binarie
def dice_coefficient(mask1, mask2):
    # Convert the data to binary arrays (0 or 1)
    mask1 = mask1.astype(bool)
    mask2 = mask2.astype(bool)

    # Calculate the dice coefficient
    intersection = mask1 & mask2
    if mask1.sum() or mask2.sum() > 0:
        dice = 2 * intersection.sum() / (mask1.sum() + mask2.sum())
    else:
        dice = 0

    # Return the dice coefficient
    return dice


def dice_multiclass(y_free, y_fast, n_classes):
    dices = []
    for i in range(n_classes):
        mask1 = [y_free == i]
        mask2 = [y_fast == i]

        dices.append(dice_coefficient(mask1[0], mask2[0]))
    return dices


def dice_score_multiclass(y_free, y_fast, n_classes):
    """
    Calculates the Dice score for a multiclass segmentation problem.
    """
    # Ensure that the masks have the same shape
    assert y_free.shape == y_fast.shape, f"Masks have different shapes: {y_free.shape} and {y_fast.shape}."

    print(n_classes)

    # flatten the arrays

    y_fast_res = np.zeros((y_fast.size, n_classes), dtype=int)
    y_fast_res[np.arange(y_fast.size), y_fast] = 1

    y_free_res = np.zeros((y_free.size, n_classes), dtype=int)
    y_free_res[np.arange(y_free.size), y_free] = 1

    print(y_free_res.shape)
    n_classes = y_free.shape[-1]
    dice_scores = []

    print(y_free.shape)

    for i in range(n_classes):
        y_free_class = y_free_res[..., i]
        y_fast_class = y_fast_res[..., i]
        intersection = np.sum(y_free_class * y_fast_class)

        if y_free_class.sum() or y_fast_class.sum() > 0:
            dice = (2. * intersection) / (np.sum(y_free_class) + np.sum(y_fast_class))
        else:
            dice = 0

        dice_scores.append(dice)

    return dice_scores
