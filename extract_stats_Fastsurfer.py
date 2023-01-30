import zipfile
import os
import pandas as pd
import shutil
import csv
import re


def extract_path(filename, base_path):
    all_path = []

    for path, subdirs, files in os.walk(base_path):
        for name in files:
            all_path.append(os.path.join(path, name))

    subjs_path = []

    for p in all_path:
        if '/stats/' in p:
            if filename in p:
                subjs_path.append(p)

    return subjs_path


def stats(subj_paths):

    df_dict = {}

    for path in subj_paths:
        with open(path, "r") as file:
            data = file.readlines()

        first = True

        for i, line in enumerate(data):

            # parte 1
            match = re.search(r"# Measure (\w+),\s*\w+,.*,\s*(\d+| \d+.\d+)\s*,\s*(\w+)", line)
            print(match)
            print(type(match))
            if match:
                if first:
                    df_dict[match.group(1)] = [match.group(2)]
                else:
                    df_dict[match.group(1)].append(
                        match.group(2))

            # parte 2
            if not line.startswith("#"):
                values = line.strip().split("\t")
                if first:
                    df_dict[values[4] + " volume"] = [values[3]]
                else:
                    df_dict[values[4]].append(values[4])  # mette le misure in due liste e i nomi delle misure anche

            first = False

        return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    base_path = ''

    # the filename of the stats to extract
    filename = ''

    subj_paths = extract_path(filename, base_path)
    stats(subj_paths).to_csv("aseg.csv")

