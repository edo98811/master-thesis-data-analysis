import data_manipulation as dm
import data_visualization as dv
import numpy as np

def main():
    data = dm.load_dict("/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/utilities/metrics.json")

    avg_dices = []

    count = 0
    for i,subj in enumerate(data.keys()):
        count = count +1
        print(data[subj]["dice_x"][0])

        dices = np.zeros(len(data[subj]["dice_x"][0]))
        avg_dice_class_n = []

        for class_n in range(len(dices)):
            dice_values_class_n = [data[subj]["dice_x"][i][class_n] for i in range(len(data[subj]["dice_x"][i]))]
            # print(dice_values_class_n)
            avg_dice_class_n.append(dv.avg_dice(dice_values_class_n))
        avg_dices.append(avg_dice_class_n)
        #print(avg_dices_per_class)
        if count > 0:
            break
        #for j,slice in enumerate(data[subj]["dice_x"]):
        #    dices[j] = dv.avg_dice(slice)

        dv.plot_dice(range(len(avg_dice_class_n)), avg_dice_class_n)

    
if __name__ == "__main__":
    main()