import csv

import pandas as pd
df = pd.read_csv('numbers.csv', index_col=0)
print(df)
print(df.index[-1])