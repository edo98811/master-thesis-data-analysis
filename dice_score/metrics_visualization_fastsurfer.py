import data_manipulation as dm
import data_visualization as dv
import numpy as np

def main():
    data = dm.load_dict("/old scripts/metrics.json")

    avg_dices = []

    count = 0
    for i,subj in enumerate(data.keys()):
        count = count + 1
        # print(data[subj]["dice_x"][0])

        dices = np.zeros(len(data[subj]["dice_x"][0]))
        avg_dice_class_n = []

        # calculate the dice values per class and not per slice
        for class_n in range(len(dices)):
            dice_values_class_n = [data[subj]["dice_x"][j][class_n] for j in range(len(data[subj]["dice_x"]))]

            avg_dice_class_n.append(dv.avg_dice(dice_values_class_n))

        avg_dices.append(avg_dice_class_n) # list of lists di tutti gli average dices
        del avg_dice_class_n

        # n of subjects
        if count > 10:
            break


    # plot
    class_n_list = []
    for j in range(len(avg_dices[0])):
        class_n_list.append(j)

    dv.plot_dice_labels(class_n_list,avg_dices)

if __name__ == "__main__":
    main()