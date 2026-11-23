import pandas as pd

FILENAME = "rawdata.csv"

df = pd.read_csv(FILENAME)
print(df.loc[df['matchType'] == "Private room"])