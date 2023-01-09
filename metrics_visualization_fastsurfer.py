import data_manipulation as dm
import data_visualization as dv
import numpy as np

def main():
    data = dm.load_dict("metrics.json")
    avg_dices = np.zeros(len(data))

    for subj in data:
        avg_dices.append(dv.avg_dice(subj))
    
    dv.plot_dice(data.keys(), avg_dices)

    

if __name__ == "__main__":
    main()