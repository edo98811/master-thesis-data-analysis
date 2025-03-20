import json

from math import log
import pandas as pd
from scipy.stats import shapiro


def main(input):
    stack = []
    ToInsert = False

    for element in input:
        if element == "(":
            ToInsert = True
        elif element == ")":
            stack.pop()
        elif element.isnumeric():
            if ToInsert:
                stack.append(int(element))
                ToInsert = False
        elif element == "+":
            for i, e in enumerate(stack):
                stack[i] = int(e) + (i + 1)
        elif element == "-":
            for i, e in enumerate(stack):
                stack[i] = int(e) - (i - 1)
    return sum(stack)

def main2( ):
    inp =  [0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1]
    ou = [0.2628, 0.8054, 0.5164, 0.3188, 0.7841, 0.0636, 0.3322, 0.2479,  0.0226, 0.0260, 0.7305, 0.6972, 0.0105, 0.8633, 0.5260, 0.5806]
    BCE = 0
    for i,o in zip(inp,ou):
        BCE += (-i*log(o)) - (1 - i)*log(1-o)

    print(BCE)

def main3():
    url = "https://gist.githubusercontent.com/fgiobergia/ee89baf09999a8d4b3a464ed98baa4d3/raw/3cd6e1c5aab0abe718f12a869c181c5e82307d99/dataset.csv"
    df = pd.read_csv(url, header=None)

    for i, row in df.iterrows():
        s, p = shapiro(row)

        if p > 0.06:
            print(f"{i} - {p}")

    print(df.head())



if __name__ == "__main__":
    main3()

def ciao():
    with open("input.json", "r") as user_file:
        parsed_json = json.load(user_file)

    result = {}

    for input in parsed_json.keys():
       result[input] = main(parsed_json[input])

    json_object = json.dumps(result, indent=4)

    with open('result.json', 'w') as f:
        f.write(json_object)
