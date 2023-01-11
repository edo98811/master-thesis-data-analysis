from scipy.spatial.distance import euclidean

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


def dice_score_multiclass(y_true, y_pred):
    """
    Calculates the Dice score for a multiclass segmentation problem.
    """
    # Ensure that the masks have the same shape
    assert y_true.shape == y_pred.shape, f"Masks have different shapes: {y_true.shape} and {y_pred.shape}."

    n_classes = y_true.shape[-1]
    dice_scores = []

    for i in range(n_classes):
        y_true_class = y_true[..., i]
        y_pred_class = y_pred[..., i]
        intersection = np.sum(y_true_class * y_pred_class)
        if y_true_class.sum() or y_pred_class.sum() > 0:
            dice = (2. * intersection) / (np.sum(y_true_class) + np.sum(y_pred_class))

        dice_scores.append(dice)

    return dice_scores