
class Dataset:
    def __init__(self, df_subj):
        self.df = "read_csv"

    def get_subj_list(self):
        pass

    def get_processed(self):
        pass

    def calculate_stats(self, stats_filename, save_filename, subj_list, _type):
        stat_file_paths = extract_path(stats_filename, subj_list)

        if stat_file_paths:
            print("stats file found for " + str(len(stat_file_paths)) + " subjects")
            if _type == 0:
                stats_aseg(stat_file_paths).to_csv(SAVE_PATH + save_filename, index=False)
            elif _type == 1:
                stats_aparcDTK(stat_file_paths).to_csv(SAVE_PATH + save_filename, index=False)
        else:
            print("no file found")


    def extract_path(self, filename, subj_list):
        # set of all the subjects for easier computation
        subj_list_numbers = set(subj_list)

        # creates a list with all the subjects that are in the list
        # for s in subj_list:
        #     if len(s.split("/")) > 4:
        #         subj_list_numbers.add(s.split("/")[-4])
        # print(subj_list_numbers)

        paths_found = []
        for path, subdirs, files in os.walk(BASE_PATH):
            if path.split("/")[-1] == 'stats' and path.split("/")[-2] in subj_list_numbers:
                for name in files:
                    if name == filename:
                        paths_found.append(path + "/" + name)

        if not paths_found:
            return False

        return paths_found


    def stats_aseg(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            print("extracting stats for subject " + str(n + 1) + ", path:" + path)

            # saving the subject name
            df_dict["ID"].append(path.split("/")[-3])

            # opens file and loads it as list of lines
            with open(path, "r") as file:
                data = file.readlines()

            # iterating though the lines
            for i, line in enumerate(data):

                # part 1
                match = re.match(r"^# Measure (\w+).+(\d+ | \d+\.\d+),\s.+$", line)

                if match:
                    # if it's the first iteration it creates the lists, assumes all the files are the same (which should be)
                    if not n:
                        df_dict[match.group(1)] = [match.group(2)]
                    else:
                        if match.group(1) in df_dict.keys():
                            df_dict[match.group(1)].append(match.group(2))
                        else:
                            df_dict[match.group(1)] = ["NaN" for _ in range(n)]  # if there are NaN
                            df_dict[match.group(1)].append(match.group(2))
                # part 2
                if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                    values = line.strip().split()  # extracts the words and puts them in lists

                    if not n:
                        df_dict[values[4] + "_volume_mm3"] = [
                            values[3]]  # the volume_mm3 is in column 4(index 3) name in column 5
                    else:
                        if f"{values[4]}_volume_mm3" in df_dict.keys():
                            df_dict[f"{values[4]}_volume_mm3"].append(values[3])
                        else:
                            df_dict[values[4] + "_volume_mm3"] = ["NaN" for _ in range(n)]
                            df_dict[f"{values[4]}_volume_mm3"].append(values[3])

            # if some columns have different length at the end pf a cycle
            for key in df_dict.keys():
                if len(df_dict[key]) != n + 1:
                    df_dict[key].append("NaN")

        # # if some columns have different length
        # for key in df_dict.keys():
        #    if len(df_dict[key]) != n+1:
        #        for _ in range(n+1 - len(df_dict[key])):
        #            df_dict[key].append("NaN")

        # dm.write_dict(df_dict,"prova_df_dict.json")
        return pd.DataFrame.from_dict(df_dict, orient='columns')


    def stats_aparcDTK(self, subj_paths):
        df_dict = {"ID": []}

        for n, path in enumerate(subj_paths):
            print("extracting stats for subject " + str(n + 1) + ", path:" + path)

            # saving the subject name
            df_dict["ID"].append(path.split("/")[-3])

            # opens file and loads it as list of lines
            with open(path, "r") as file:
                data = file.readlines()

            # iterating though the lines
            for i, line in enumerate(data):

                # part 1
                match = re.match(r"^# Measure (\w+,\s\w+).+(\d+ | \d+\.\d+),\s.+$", line)

                if match:
                    # if it's the first iteration it creates the lists, assumes all the files are the same (which should be)
                    if not n:
                        df_dict[match.group(1).replace(" ", "")] = [match.group(2)]
                    else:
                        if match.group(1).replace(" ", "") in df_dict.keys():
                            df_dict[match.group(1).replace(" ", "")].append(match.group(2))
                        else:
                            df_dict[match.group(1).replace(" ", "")] = ["NaN" for _ in range(n)]
                            df_dict[match.group(1).replace(" ", "")].append(match.group(2))

                # part 2
                if not line.startswith("#"):  # the last table is the only part in which the lines don't start with #
                    values = line.strip().split()  # extracts the words and puts them in lists

                    if not n:
                        df_dict[values[0] + "_mean_thickness_mm"] = [
                            values[4]]  # the thickness is in column 4(index 3) name in column 5
                    else:
                        if f"{values[0]}_mean_thickness_mm" in df_dict.keys():
                            df_dict[f"{values[0]}_mean_thickness_mm"].append(values[4])
                        else:
                            df_dict[values[0] + "_mean_thickness_mm"] = ["NaN" for _ in range(n)]
                            df_dict[values[0] + "_mean_thickness_mm"].append(values[4])

                    if not n:
                        df_dict[values[0] + "_mean_area_mm2"] = [
                            values[2]]  # the area is in column 3(index 2) name in column 5
                    else:
                        if f"{values[0]}_mean_area_mm2" in df_dict.keys():
                            df_dict[f"{values[0]}_mean_area_mm2"].append(values[2])
                        else:
                            df_dict[values[0] + "_mean_area_mm2"] = ["NaN" for _ in range(n)]
                            df_dict[values[0] + "_mean_area_mm2"].append(values[2])

            # if some columns have different length at the end of a cycle
            for key in df_dict.keys():
                if len(df_dict[key]) != n + 1:
                    df_dict[key].append("NaN")

        dm.write_dict(df_dict, "old scripts/prova_df_dict.json")

        # # if some columns have different length
        # for key in df_dict.keys():
        #    if len(df_dict[key]) != n+1:
        #        for _ in range(n + 1 - len(df_dict[key])):
        #            df_dict[key].append("NaN")

        return pd.DataFrame.from_dict(df_dict, orient='columns')


if __name__ == "__main__":
    main()

class Stats(Dataset):
    def __init__(self, df_subj, df_stats, SF=0.05):
        super().__init__(df_subj)
        self.df_stats = df_stats
        self.SF = SF

    def bonferroni_correction_param(self, queries):
        tot = 0
        for query in queries:
            with open(BASE_PATH + query + ".csv") as fp:
                for (count, _) in enumerate(fp, 1):
                    pass
                print(count)
                tot += count

        return SIGNIFICANCE_THRESHOLD / tot

    def bonferroni_correction(self, queries):
        updated_ST = bonferroni_correction_param(queries)
        print(updated_ST)
        for query in queries:
            df = pd.read_csv(BASE_PATH + query + ".csv")
            for i, row in df.iterrows():
                if row[1] < updated_ST:
                    row[3] = f"p-value: {row[0]} - null hypothesis rejected, means are not statistically equal"
                    row[2] = 1
                if row[4] < updated_ST:
                    row[6] = f"p-value: {row[3]} - null hypothesis rejected, the datasets have a different distribution"
                    row[5] = 1
                df.iloc[i, :] = row
            df.to_csv(BASE_PATH + f"{query}_bonferroni_corrected.csv")

    def stat_test(self, _queries, _df1_path, _df2_path, _subj_table, r_all):
        # input: query, df1 name, df2 name, subj_table, list of all test results
        _df1 = pd.read_csv(BASE_PATH + _df1_path)
        _df2 = pd.read_csv(BASE_PATH + _df2_path)

        table_tested_name = _df1_path.split(".")[-2]

        max_len = min(len(_df1.axes[1]), len(_df2.axes[1]))
        for query in _queries:

            subjects_list = _subj_table.query(query)["ID"].tolist()
            for i, s in enumerate(subjects_list):
                subjects_list[i] = "sub-" + s
            print(f"query -> {query} on table returned these values:")
            print(subjects_list)
            print("dataset 1 not filtered")
            print(_df1.head())

            _df1_filtered = _df1.loc[_df1['ID'].isin(subjects_list)]
            _df2_filtered = _df2.loc[_df2['ID'].isin(subjects_list)]

            print("filtered dataset 1 according to subjects returned in queries")
            print(_df2_filtered.head())
            print("filtered dataset 2")
            print(_df2_filtered.head())
            print("COMPUTING STATS FOR FIRST QUERY...")

            for column_to_compare in range(2, max_len):
                a, b = get_column(column_to_compare, _df1_filtered, _df2_filtered)
                if a.any() and b.any():
                    r1, p1, o1 = mann_whitney(a, b)
                    r2, p2, o2 = t_test(a, b)

                    if isinstance(column_to_compare, int):
                        column_to_compare_name = _df1_filtered.columns[column_to_compare]

                        r_all.append({"name": f"{table_tested_name} {column_to_compare_name}",
                                      "mann_whitney": {"result": r1,
                                                       "p_value": p1,
                                                       "outcome": o1},
                                      "t_test": {"result": r2,
                                                 "p_value": p2,
                                                 "outcome": o2}})

                    if isinstance(column_to_compare, str):
                        r_all.append({"name": f"{table_tested_name} {column_to_compare}",
                                      "mann_whitney": {"result": r1,
                                                       "p_value": p1,
                                                       "outcome": o1},
                                      "t_test": {"result": r2,
                                                 "p_value": p2,
                                                 "outcome": o2}})
                else:
                    print(f"no data in category {column_to_compare}")
            save_csv(r_all, f"{query}.csv")

    def save_csv(self, list_to_save, _name):
        df = pd.DataFrame()

        for item in list_to_save:
            df = pd.concat([df, pd.DataFrame({"mann_whitney p_value": item["mann_whitney"]["p_value"],
                                              "mann_whitney outcome": item["mann_whitney"]["outcome"],
                                              "mann_whitney message": item["mann_whitney"]["result"],
                                              "t_test p_value": item["t_test"]["p_value"],
                                              "t_test outcome": item["t_test"]["outcome"],
                                              "t_test message": item["t_test"]["result"],
                                              "significance_threshold_used": SIGNIFICANCE_THRESHOLD
                                              }, index=[item["name"]])])

        df.to_csv(BASE_PATH + _name)  # , index=False

    def get_column(self, column_to_compare, df1, df2):
        if isinstance(column_to_compare, int):
            a = df1.iloc[:, column_to_compare]
            b = df2.iloc[:, column_to_compare]

        if isinstance(column_to_compare, str):
            a = df1.loc[:, column_to_compare]
            b = df2.loc[:, column_to_compare]

        return a, b

    def t_test(self, a, b):
        # a, b = get_column(column_to_compare, df1, df2)

        if "NaN" in a or "NaN" in b:
            print("could not compute")
            return "result could not be computed", "NaN", "NaN"

        t_stat, p_value = stats.ttest_ind(a, b)

        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected, means are statistically equal"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected, means are not statistically equal"
            outcome = 1

        return result, p_value, outcome

    def mann_whitney(self, a, b):
        # a, b = get_column(column_to_compare, df1, df2)

        if "NaN" in a or "NaN" in b:
            return "result could not be computed", "NaN", "NaN"

        # df1.to_csv("dataset_uniti_test.csv", index=False)

        t_stat, p_value = stats.mannwhitneyu(a, b)

        # p value is the likelihood that these are the same
        if p_value > 0.05:
            result = f"p-value: {p_value} - null hypothesis cannot be rejected, the datasets have the same distribution"
            outcome = 0
        else:
            result = f"p-value: {p_value} - null hypothesis rejected, the datasets have a different distribution"
            outcome = 1

        return result, p_value, outcome

