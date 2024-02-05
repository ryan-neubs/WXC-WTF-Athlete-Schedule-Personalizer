from math import isnan
import pandas as pd

wo = pd.read_excel("test.xlsx")
rows = wo.values.tolist()
for row in rows:
    if type(row[-1]) == str:
        print(row[-1])