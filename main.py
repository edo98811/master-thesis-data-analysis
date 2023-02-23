import FastsurferTesting as ft
import pandas as pd

ADNI_PATH =
OASIS_PATH =
BASE_PATH =

def main():

    table = ft.Table(pd.load_csv())

    stats_healthy = ft.Stats(table, "healthy", "'main condition'== NC", b_path=BASE_PATH)
    stats_MC = ft.Stats(table, "healthy", "'main condition'!= NC", b_path=BASE_PATH)



if __name__ =="__main__":
    main()