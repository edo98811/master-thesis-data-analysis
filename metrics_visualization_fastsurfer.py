import data_manipulation as dm
import data_visualization as dv

def main():
    data = dm.load_dict("metrics.json")

    for subj in data:
        dv.plot_dice(subj)

if __name__ == "__main__":
    main()